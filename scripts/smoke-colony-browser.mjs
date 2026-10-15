// Actual public WebGL acceptance on a software WebGL-capable Actions browser.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const sharp=require('sharp');
const sha=process.argv[2],out=process.argv[3];
if(!/^[a-f0-9]{40}$/.test(sha??'')||!out)throw Error('Exact distribution SHA and output required');
const manifest=JSON.parse(await fs.readFile('docs/head/UNITY_ARTIFACT_MANIFEST.json','utf8'));
const source=manifest.games.find(g=>g.game==='colony-racer').unitySourceSha;
const url='https://unity-games.wos.ktsys.jp/02/colony-racer/';
const report={complete:false,pass:false,distributionSha:sha,unitySourceSha:source,url,observations:[],checks:[],errors:[],pageErrors:[],environment:'Ubuntu Actions Chromium software WebGL; not a physical phone'};
await fs.mkdir(out,{recursive:true});
let browser,p;
const state=p=>p.evaluate(()=>window.ColonyRacerWebPreview?.snapshot());
const observed=(name,snapshot)=>report.observations.push({name,pass:true,observedUtc:new Date().toISOString(),tool:'Playwright Chromium',snapshot});
const wait=(p,fn,timeout=45000)=>p.waitForFunction(fn,null,{timeout,polling:250});
try{
 browser=await chromium.launch({headless:true,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,hasTouch:true,isMobile:true});
 p=await context.newPage();
 p.on('console',m=>{if(m.type()==='error')report.errors.push(m.text());});p.on('pageerror',e=>report.pageErrors.push(String(e)));
 await p.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
 await wait(p,()=>window.ColonyRacerWebPreview?.snapshot().ready||window.ColonyRacerWebPreview?.snapshot().loadError,300000);
 if((await state(p)).loadError)throw Error('Unity load failed');
 await p.locator('#start').click({timeout:120000});
 await wait(p,()=>{const s=window.ColonyRacerWebPreview.snapshot();return !s.paused&&s.telemetry?.reflectionReady;},180000);
 if(!(await p.title()).includes('Colony Racer')||p.url()!==url)throw Error('Wrong public page');
 observed('loaded',await state(p));
 await p.screenshot({path:path.join(out,'portrait-started.png')});
 await p.setViewportSize({width:844,height:390});
 async function shot(name){
  const bytes=await p.screenshot({path:path.join(out,name+'.png')});
  const stats=await sharp(bytes).extract({left:211,top:130,width:422,height:140}).stats();
  const variation=stats.channels.slice(0,3).reduce((sum,c)=>sum+c.stdev,0);
  report.checks.push({name:'render '+name,pass:variation>25,variation});
  if(variation<=25)throw Error('Missing public WebGL scene');
 }
 await shot('loaded');
 for(const name of ['Core','East','West']){
  await p.locator(`[data-district="${name}"]`).click();
  await p.waitForFunction(n=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.district===n&&t.grounded;},name,{timeout:60000,polling:250});
 }
 observed('districts',await state(p));
 for(const [selector,label] of [['#expressway','Expressway'],['[data-ring="0"]','S LOOP'],['[data-ring="1"]','CENTRAL LOOP'],['[data-ring="2"]','N LOOP']]){
  await p.locator(selector).click();
  await p.waitForFunction(n=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.district===n&&t.grounded;},label,{timeout:60000,polling:250});
  report.checks.push({name:label,pass:true,snapshot:await state(p)});await shot(label.replaceAll(' ','-'));
 }
 await p.locator('#expressway').click();
 await p.keyboard.down('w');
 await wait(p,()=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.throttle>.9&&t.speedKmh>10;},60000);
 observed('accelerate',await state(p));await p.keyboard.up('w');
 await p.keyboard.down('Space');
 await wait(p,()=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.brake>.9&&t.speedKmh<1;},60000);
 observed('brake',await state(p));await p.keyboard.up('Space');
 await p.keyboard.down('w');await p.keyboard.down('d');
 await wait(p,()=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.steer>.5&&Math.abs(t.headingDegrees)>.2;},45000);
 observed('steer',await state(p));await p.keyboard.up('w');await p.keyboard.up('d');
 await p.locator('#reset').click();
 await wait(p,()=>{const t=window.ColonyRacerWebPreview.snapshot().telemetry;return t.district==='Core'&&t.grounded&&t.speedKmh<1;});
 observed('reset',await state(p));await shot('reset');
 if(report.errors.length||report.pageErrors.length)throw Error('Public runtime errors');
 report.complete=true;report.pass=true;
}catch(e){
 report.failure=String(e.stack||e);process.exitCode=1;
 if(p){
  try{report.failedSnapshot=await state(p);}catch{}
  try{await p.screenshot({path:path.join(out,'failure.png'),timeout:10000});}catch{}
 }
}
finally{
 await fs.writeFile(path.join(out,'acceptance.json'),JSON.stringify(report,null,2)+'\n');
 if(browser)await browser.close();
 console.log(JSON.stringify({complete:report.complete,pass:report.pass,failure:report.failure}));
}
