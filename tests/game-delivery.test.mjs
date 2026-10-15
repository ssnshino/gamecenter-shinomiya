import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { gzipSync, brotliCompressSync } from 'node:zlib';
import {contentTypeFor,contentEncodingFor} from '../apps/unity-web/src/lib/files.ts';
import { verifyGame, safeRelative, manifest, unityProvenance } from '../scripts/verify-game-delivery.mjs';
test('native Brotli scripts and WebAssembly retain executable MIME and encoding',()=>{
  for(const ext of ['br','gz']){
    assert.equal(contentTypeFor(`Build/game.wasm.${ext}`),'application/wasm');
    assert.match(contentTypeFor(`Build/game.framework.js.${ext}`),/^application\/javascript/);
    assert.equal(contentTypeFor(`Build/game.data.${ext}`),'application/octet-stream');
    assert.equal(contentEncodingFor(`Build/game.data.${ext}`),ext==='br'?'br':'gzip');
  }
  assert.equal(contentEncodingFor('Build/legacy.data.unityweb'),null);
});
export async function fixture() {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'game-delivery-'));
  const put = async (rel, value) => { await fs.mkdir(path.dirname(path.join(root, rel)), { recursive: true }); await fs.writeFile(path.join(root, rel), value); };
  await put('index.html', 'var buildUrl="Build";var loaderUrl=buildUrl+"/a.loader.js"; const c={dataUrl:buildUrl+"/a.data.gz",frameworkUrl:buildUrl+"/a.framework.js.gz",codeUrl:buildUrl+"/a.wasm.gz"};');
  await put('Build/a.loader.js', 'loader');
  for (const ext of ['data', 'framework.js', 'wasm']) await put(`Build/a.${ext}.gz`, gzipSync(Buffer.from(ext)));
  for (const [name, obj] of Object.entries({aircraft_prefab_catalog:{version:'v1',prefabs:[{bundlePath:'AirRace/Bundles/a',prefabName:'Aircraft'}]},round_world_catalog:{version:'v1',worlds:[{bundlePath:'AirRace/Bundles/a',prefabName:'World',round:1}]},world_object_catalog:{version:'v1',objects:[]},airrace_rounds:{1:{gates:[]}}})) await put(`StreamingAssets/AirRace/${name}.json`, JSON.stringify(obj));
  await put('StreamingAssets/AirRace/Bundles/a', 'bundle');
  return {root,put};
}
test('valid package hashes compressed and decompressed bytes', async () => {const {root}=await fixture();const m=await verifyGame(root,'airrace3d');assert.equal(m.files.length,10);const w=m.files.find(x=>x.path.endsWith('wasm.gz'));assert.notEqual(w.sha256,w.httpSha256);});
test('missing bundle fails closed',async()=>{const {root}=await fixture();await fs.unlink(path.join(root,'StreamingAssets/AirRace/Bundles/a'));await assert.rejects(verifyGame(root,'airrace3d'),/Missing referenced/);});
test('unsafe paths rejected',()=>{for(const p of ['../a','/a','a/../b','a\\b','https://x/a','a%2fb','a?x','a//b'])assert.throws(()=>safeRelative(p));});
test('symlink escape rejected',async()=>{const {root}=await fixture();await fs.symlink('/etc/passwd',path.join(root,'escape'));await assert.rejects(verifyGame(root,'airrace3d'),/Symlink/);});
test('malformed catalog rejected',async()=>{const {root,put}=await fixture();await put('StreamingAssets/AirRace/round_world_catalog.json','{');await assert.rejects(verifyGame(root,'airrace3d'));});
test('unsupported HTML fails rather than evaluates JS',async()=>{const {root,put}=await fixture();await put('index.html','var buildUrl="https://evil.example";');await assert.rejects(verifyGame(root,'airrace3d'),/Unsupported/);});
test('corrupt gzip rejected',async()=>{const {root,put}=await fixture();await put('Build/a.wasm.gz','bad');await assert.rejects(verifyGame(root,'airrace3d'));});
test('source SHA is mandatory',async()=>{await assert.rejects(manifest('.',undefined),/SOURCE_SHA/);});

import { createServer } from 'node:http';
import { smoke } from '../scripts/smoke-game-delivery.mjs';
async function smokeFixture(brotli = false) {
  const {root}=await fixture();
  if(brotli){
    await fs.writeFile(path.join(root,'index.html'),(await fs.readFile(path.join(root,'index.html'),'utf8')).replaceAll('.gz','.br'));
    for(const ext of ['data','framework.js','wasm']){
      await fs.writeFile(path.join(root,`Build/a.${ext}.br`),brotliCompressSync(Buffer.from(ext)));
      await fs.unlink(path.join(root,`Build/a.${ext}.gz`));
    }
  }
  const repo=await fs.mkdtemp(path.join(os.tmpdir(),'game-smoke-'));
  const target=path.join(repo,'apps/unity-web/public/airrace3d');await fs.mkdir(path.dirname(target),{recursive:true});await fs.cp(root,target,{recursive:true});
  await fs.cp(root,path.join(repo,'apps/unity-web/public/colony-racer'),{recursive:true});
  const m={schema:1,sourceSha:'a'.repeat(40),games:[await verifyGame(target,'airrace3d'),await verifyGame(target,'colony-racer')]};
  let corrupt=false, badHeader=false;
  const server=createServer(async(req,res)=>{
    try {
      const url=new URL(req.url,'http://localhost');
      if(url.pathname==='/healthz'){res.setHeader('content-type','application/json');res.end(JSON.stringify({ok:true,service:'gamecenter-shinomiya-unity-web'}));return;}
      if(/^\/api\/(airrace3d|colony-racer)\//.test(url.pathname)){
        const names={'round-world-catalog':'round_world_catalog.json','aircraft-prefab-catalog':'aircraft_prefab_catalog.json','world-object-catalog':'world_object_catalog.json'};
        const name=names[url.pathname.split('/').at(-1)];res.setHeader('content-type','application/json');res.end(await fs.readFile(path.join(target,'StreamingAssets/AirRace',name)));return;
      }
      const rel=url.pathname.replace(/^\/(airrace3d|colony-racer)\//,'');
      const encoding=contentEncodingFor(rel);if(encoding&&!badHeader)res.setHeader('content-encoding',encoding);
      res.setHeader('content-type',contentTypeFor(rel));
      res.end(corrupt&&rel==='Build/a.loader.js'?'wrong':await fs.readFile(path.join(target,rel)));
    }catch{res.statusCode=404;res.end('not found');}
  });
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  return {m,repo,url:`http://127.0.0.1:${server.address().port}`,close:()=>new Promise(resolve=>server.close(resolve)),corrupt:()=>{corrupt=true;},badHeader:()=>{badHeader=true;}};
}
test('HTTP smoke verifies gzip decoded hash and API equivalence',async()=>{const s=await smokeFixture();try{await smoke(s.m,s.url,s.repo);}finally{await s.close();}});
test('HTTP smoke verifies native Brotli decoded hash and executable MIME',async()=>{const s=await smokeFixture(true);try{await smoke(s.m,s.url,s.repo);}finally{await s.close();}});
test('HTTP smoke rejects missing native Brotli header',async()=>{const s=await smokeFixture(true);s.badHeader();try{await assert.rejects(smoke(s.m,s.url,s.repo),/brotli header/);}finally{await s.close();}});
test('HTTP smoke rejects stale public artifact',async()=>{const s=await smokeFixture();s.corrupt();try{await assert.rejects(smoke(s.m,s.url,s.repo),/mismatch/);}finally{await s.close();}});
test('HTTP smoke rejects missing gzip header',async()=>{const s=await smokeFixture();s.badHeader();try{await assert.rejects(smoke(s.m,s.url,s.repo),/gzip header/);}finally{await s.close();}});

test('empty smoke manifest rejected',async()=>{await assert.rejects(smoke({schema:1,sourceSha:'a'.repeat(40),games:[]},'http://127.0.0.1','.'),/two-game/);});
test('catalog entries must contain required bundle and prefab',async()=>{const {root,put}=await fixture();await put('StreamingAssets/AirRace/aircraft_prefab_catalog.json',JSON.stringify({version:'v1',prefabs:[{}]}));await assert.rejects(verifyGame(root,'airrace3d'),/Invalid prefab/);});
test('null round rejected',async()=>{const {root,put}=await fixture();await put('StreamingAssets/AirRace/airrace_rounds.json',JSON.stringify({1:null}));await assert.rejects(verifyGame(root,'airrace3d'),/Invalid rounds/);});

test('game root symlink rejected',async()=>{const {root}=await fixture();const parent=await fs.mkdtemp(path.join(os.tmpdir(),'root-symlink-'));const link=path.join(parent,'linked');await fs.symlink(root,link);await assert.rejects(verifyGame(link,'airrace3d'),/root symlink/);});

test('Unity provenance rejects unperformed and ambiguous source claims',()=>{
  assert.throws(()=>unityProvenance('a'.repeat(40),false),/provenance/);
  assert.throws(()=>unityProvenance('working-tree',true),/provenance/);
});
test('Colony provenance is scoped and survives ordinary manifest regeneration',async()=>{
  const {root}=await fixture();const repo=await fs.mkdtemp(path.join(os.tmpdir(),'game-provenance-'));
  await fs.mkdir(path.join(repo,'apps/unity-web/public'),{recursive:true});
  for(const game of ['airrace3d','colony-racer']) await fs.cp(root,path.join(repo,'apps/unity-web/public',game),{recursive:true});
  const m=await manifest(repo,'a'.repeat(40),{colonyProvenance:unityProvenance('b'.repeat(40),true)});
  assert.equal(m.unitySourceSha,null);assert.equal(m.unityBuildPerformed,true);
  assert.equal(m.games[0].unitySourceSha,undefined);assert.equal(m.games[1].unitySourceSha,'b'.repeat(40));
  await fs.mkdir(path.join(repo,'docs/head'),{recursive:true});
  await fs.writeFile(path.join(repo,'docs/head/UNITY_ARTIFACT_MANIFEST.json'),JSON.stringify(m));
  assert.deepEqual(await manifest(repo,'a'.repeat(40)),m);
  assert.equal((await manifest(repo,'c'.repeat(40))).unityBuildPerformed,false);
});

async function literalFixture() {
  const f=await fixture();
  await f.put('preview.css','body{margin:0}');await f.put('preview.js','window.previewReady=true;');
  for(const ext of ['data','framework.js','wasm']) await f.put(`Build/p.${ext}.unityweb`,gzipSync(Buffer.from(ext)));
  const html='<link href="preview.css" rel="stylesheet"><script src="preview.js"></script><script>const config={loaderUrl:"Build/a.loader.js",dataUrl:"Build/p.data.unityweb",frameworkUrl:"Build/p.framework.js.unityweb",codeUrl:"Build/p.wasm.unityweb"};</script>';
  await f.put('index.html',html);
  return {...f,html};
}
test('literal local Build template inventories fallback files and local controller assets',async()=>{
  const {root}=await literalFixture();const m=await verifyGame(root,'colony-racer');
  assert.ok(m.required.includes('preview.css'));assert.ok(m.required.includes('preview.js'));assert.ok(m.required.includes('Build/p.wasm.unityweb'));
  const file=m.files.find(f=>f.path==='Build/p.data.unityweb');assert.equal(file.sha256,file.httpSha256);
});
test('literal Build references reject absolute URLs traversal and queries',async()=>{
  for(const value of ['https://bad.example/a.wasm','/Build/a.wasm','Build/../a.wasm','Build/a.wasm?version=1']){
    const {root,put,html}=await literalFixture();await put('index.html',html.replace('Build/p.wasm.unityweb',value));
    await assert.rejects(verifyGame(root,'colony-racer'),/Unsafe artifact/);
  }
});
test('literal preview fails when referenced controller or build file is missing',async()=>{
  for(const missing of ['preview.css','preview.js','Build/p.wasm.unityweb']){
    const {root}=await literalFixture();await fs.unlink(path.join(root,missing));
    await assert.rejects(verifyGame(root,'colony-racer'),/Missing referenced file/);
  }
});
test('literal preview cannot replace its local controller script with a remote URL',async()=>{
  const {root,put,html}=await literalFixture();await put('index.html',html.replace('src="preview.js"','src="https://bad.example/preview.js"'));
  await assert.rejects(verifyGame(root,'colony-racer'),/Unsafe artifact/);
});

