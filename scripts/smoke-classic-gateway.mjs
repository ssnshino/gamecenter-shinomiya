import assert from 'node:assert/strict';
const base = 'https://unity-games.wos.ktsys.jp';
for (const path of ['/', '/healthz', '/01/', '/01/api/status', '/02/']) {
  const r = await fetch(base + path, { signal: AbortSignal.timeout(15000), redirect: 'error', cache: 'no-store' });
  assert.equal(r.status, 200, path);
  assert.ok((await r.text()).length, path);
}
const redirect = await fetch('https://rust-sandbox.wos.ktsys.jp/', {signal: AbortSignal.timeout(15000),redirect:'manual'});
assert.equal(redirect.status,308);
assert.equal(redirect.headers.get('location'),base+'/01/');
await new Promise((resolve, reject) => {
  const ws = new WebSocket('wss://unity-games.wos.ktsys.jp/01/ws');
  const timer = setTimeout(() => { ws.close(); reject(Error('Classic WebSocket state timeout')); }, 15000);
  ws.addEventListener('error', () => { clearTimeout(timer); reject(Error('Classic WebSocket failed')); });
  ws.addEventListener('message', event => {
    try { JSON.parse(event.data); clearTimeout(timer); ws.close(); resolve(); }
    catch (error) { clearTimeout(timer); ws.close(); reject(error); }
  }, {once:true});
});
console.log('Portal/API/redirect/Classic WebSocket passed; no scores posted. Browser interaction remains separate.');
