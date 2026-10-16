"""One reviewed recovery only; frozen guard and original receipt stay unchanged."""
import copy,hashlib,json,pathlib,subprocess,importlib.util,datetime
ROOT=pathlib.Path('/home/shino/source/repos/upstream/gamecenter-shinomiya')
SHA='c6ad33dbb2507cd22c36c207b70f6679bbb368d3'
ORIGINAL='unity-colony-'+SHA+'-20261016T055417Z'
APPROVED={
 '/aladdin-checker-accept-20261016-1':'40219341e851e19cd24b5e692d033a0240f9c67695c426648ceaa4f2d777a45b',
 '/aladdin-checker-accept-20261016-2':'8f8e765cd1e1df4074b61fee4966229ccf8151d91cc7f3a8fff83407e2303902',
 '/aladdin-checker-accept-20261016-3':'526caf2b7159087addd0fc6a751dfa1e0f1da5edb7f89760c8440e2831cdaefb'}
IMAGE='sha256:969478aedc71d7711a5b52fc090337db7a7c80c195bc439469412447957a1243'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def reviewed(before,current):
 a={x['name']:x for x in before['containers']};b={x['name']:x for x in current['containers']}
 require(len(a)==len(before['containers']) and len(b)==len(current['containers']),'Duplicate container names')
 for name,identity in APPROVED.items():
  require(name in a and name not in b,'Approved cleanup no longer matches')
  x=a[name];require(x['id']==identity and x['image']==IMAGE,'Approved identity differs')
  require(x['running'] is False and x['state']=='exited' and x['readonly'] is True,'Approved container was not stopped/read-only')
  require(x['labels'].get('com.docker.compose.project')=='queens-checker','Unexpected project')
  require(x['mounts']==[{'Type':'bind','Source':'/home/shino/source/labs/aladdin-master-restart-20261016/checker','Destination':'/proof','RW':False}],'Unexpected reviewed mounts')
 result=copy.deepcopy(before);result['containers']=[x for x in result['containers'] if x['name'] not in APPROVED]
 def others(v):return [x for x in v['containers'] if x['name']!='/gamecenter-shinomiya-unity-web']
 require(others(result)==others(current),'Additional unrelated changes; stop review')
 return result

def run():
 import fcntl
 original=ROOT/'runtime/deploy'/ORIGINAL
 require(original.resolve()==original and original.is_dir() and not original.is_symlink(),'Unexpected receipt path')
 lock=(ROOT/'.git/classic-gateway-deploy.lock').open('a')
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 files=list(original.iterdir());require(all(x.is_file() and not x.is_symlink() for x in files),'Unexpected receipt entries')
 hashes={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in files}
 spec=importlib.util.spec_from_file_location('frozen_guard',original/'check-unity-web-release.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
 before=json.loads((original/'before.json').read_text());proposed=json.loads((original/'proposed-manifest.json').read_text());old=json.loads((original/'receipt.json').read_text())
 require(old['requestedSha']==SHA and not old['adoptionComplete'] and old['phase']=='failed-manual-rollback','Unexpected original phase')
 require(not subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True).strip(),'Dirty checkout')
 current=guard.capture(ROOT);baseline=reviewed(before,current)
 guard.check_scope(str(ROOT),current['checkoutSha'],SHA)
 guard.check_preservation(baseline,current,proposed,SHA,'provisional')
 guard.assets_match(current['actualGames'],proposed)
 built=(original/'built-image-id.txt').read_text().strip();active=next(x for x in current['containers'] if x['name']==guard.UNITY)
 require(active['image']==built,'Built image differs')
 guard.recovery_preflight(baseline,current,proposed,SHA,built,(original/'.env.release.before').read_text())
 guard.require(json.loads((original/'browser-acceptance.json').read_text())['pass'],'Original browser did not pass')
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');dest=ROOT/'runtime/deploy'/('unity-colony-'+SHA+'-'+stamp)
 require(not dest.exists(),'New receipt already exists');dest.mkdir(mode=0o700)
 for f in files:(dest/f.name).write_bytes(f.read_bytes())
 (dest/'original-before.json').write_bytes((original/'before.json').read_bytes());(dest/'original-receipt.json').write_bytes((original/'receipt.json').read_bytes())
 guard.write_json(dest/'before.json',baseline);guard.write_json(dest/'provisional.json',current)
 if (dest/'attempt-before.json').exists():raise ValueError('Unexpected previous retry baseline')
 guard.write_json(dest/'receipt.json',{'schema':1,'requestedSha':SHA,'previousCheckout':before['checkoutSha'],'publicBase':guard.PUBLIC,'phase':'awaiting-browser','adoptionComplete':False,'reviewedExternalCleanup':True,'originalReceipt':str(original)})
 guard.write_json(dest/'external-cleanup-review.json',{'schema':1,'humanConfirmation':'はい、別作業の後片付け','questionId':'call_532927641273457883505faa88eb4048','approvedRemovedContainers':APPROVED,'originalReceipt':str(original),'originalFileSha256':hashes,'reviewedBeforeSha256':hashlib.sha256((dest/'before.json').read_bytes()).hexdigest(),'frozenGuardUnmodified':(dest/'check-unity-web-release.py').read_bytes()==(original/'check-unity-web-release.py').read_bytes(),'servicesOrDataModifiedByReview':False})
 require(all(hashlib.sha256((original/n).read_bytes()).hexdigest()==h for n,h in hashes.items()),'Original receipt changed')
 print('Reviewed receipt: '+str(dest));print('Frozen original guard passed all preservation checks against exactly three human-confirmed removals. No services or data changed.')
if __name__=='__main__':run()
