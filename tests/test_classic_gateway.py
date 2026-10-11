import unittest, importlib.util, copy, tempfile, pathlib, json, os, subprocess
s=importlib.util.spec_from_file_location('guard',pathlib.Path(__file__).parents[1]/'scripts/check-classic-gateway.py'); guard=importlib.util.module_from_spec(s);s.loader.exec_module(guard)
class Guard(unittest.TestCase):
    def setUp(self):
        self.root='/home/shino/source/repos/upstream/gamecenter-shinomiya';self.sha='a'*40
        self.unity={'State':{'Running':True},'Config':{'Image':'gamecenter-shinomiya-unity-web:'+'b'*40}}
        def service(name): return {'container_name':'gamecenter-shinomiya-'+name,'networks':{'internal':{}}}
        self.c={'name':'gamecenter-shinomiya','services':{n:service(n) for n in ['classic','unity-web','gateway']},'networks':{'wos-proxy-network':{'external':True}}}
        self.c['services']['classic'].update(image='gamecenter-shinomiya-classic:'+self.sha,environment={'GIT_HASH':self.sha},read_only=True,volumes=[{'type':'bind','source':self.root+'/runtime/classic','target':'/data'}])
        self.c['services']['unity-web']['image']=self.unity['Config']['Image']
        self.c['services']['gateway'].update(image='gamecenter-shinomiya-gateway:'+self.sha,ports=[{'host_ip':'127.0.0.1','published':'18094','target':80}],networks={'internal':{},'wos-proxy-network':{}},environment={'VIRTUAL_HOST':'unity-games.wos.ktsys.jp,airrace-web.wos.ktsys.jp,rust-sandbox.wos.ktsys.jp','VIRTUAL_PORT':'80'})
    def test_valid(self):guard.check(self.c,self.unity,self.root,self.sha)
    def test_reject_mutations(self):
        mutations=[lambda c:c['services']['unity-web'].update(image='new-unity'),lambda c:c['services']['classic']['volumes'][0].update(source='/tmp/empty'),lambda c:c['services']['gateway']['networks'].pop('wos-proxy-network'),lambda c:c['services']['gateway']['ports'][0].update(host_ip='0.0.0.0'),lambda c:c['services']['gateway']['environment'].update(VIRTUAL_HOST='games.lab.ktsys.jp'),lambda c:c['services']['classic'].update(privileged=True),lambda c:c['services']['classic']['environment'].update(GIT_HASH='old')]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                c=copy.deepcopy(self.c);mutate(c)
                with self.assertRaises(AssertionError):guard.check(c,self.unity,self.root,self.sha)
    def test_unity_not_running(self):
        self.unity['State']['Running']=False
        with self.assertRaises(AssertionError):guard.check(self.c,self.unity,self.root,self.sha)
    def test_runtime_missing_or_invalid(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(AssertionError):guard.runtime_check(root)
    def test_live_data_mount(self):
        active={'State':{'Running':True},'Config':{'User':'1000:1000'},'Mounts':[{'Destination':'/data','Type':'bind','Source':self.root+'/runtime/classic','RW':True}]}
        guard.check_live_classic(active,self.root)
        active['Mounts'][0]['Source']='/another/data'
        with self.assertRaises(AssertionError):guard.check_live_classic(active,self.root)
    def test_no_destructive_commands(self):
        shell=(pathlib.Path(__file__).parents[1]/'scripts/deploy-classic-gateway.sh').read_text()
        active='\n'.join(x for x in shell.splitlines() if not x.lstrip().startswith('#'))
        self.assertNotIn('reset --hard',active);self.assertNotIn('compose down',active)
        self.assertIn('up -d --no-build --no-deps --force-recreate classic',active)
        self.assertIn('up -d --no-build --no-deps --force-recreate gateway',active)
        self.assertNotIn('up -d --no-build unity-web',active)
class DeploymentStdin(unittest.TestCase):
    def test_health_checks_and_tags_complete_when_exec_reads_stdin(self):
        # The remote script runs through bash -s. An interactive compose exec
        # must not consume the remaining script from that same standard input.
        shell = (pathlib.Path(__file__).parents[1] / 'scripts/deploy-classic-gateway.sh').read_text()
        tail = shell.split('phase=local-verification\n', 1)[1].rsplit('\nREMOTE', 1)[0]
        sha = 'a' * 40
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            stage = root / 'stage'
            stage.mkdir()
            release = root / '.env.release'
            original = 'RELEASE_TAG=' + 'b' * 40 + '\nEXISTING_SETTING=keep\n'
            release.write_text(original)
            release.chmod(0o640)
            unity = [{'Id': 'same-container', 'Image': 'same-image', 'RestartCount': 0,
                      'State': {'StartedAt': 'same-time', 'Running': True}}]
            (stage / 'unity-before.json').write_text(json.dumps(unity))
            targets = [{'State': {'Running': True}, 'Config': {
                'Image': 'gamecenter-shinomiya-' + name + ':' + sha,
                'Env': ['GIT_HASH=' + sha] if name == 'classic' else []}}
                for name in ['classic', 'gateway']]
            (stage / 'expected-targets.json').write_text(json.dumps(targets))
            setup = '''set -euo pipefail
stage="$TEST_STAGE"; sha="$TEST_SHA"; compose=(docker compose)
docker() {
  if [[ $1 == compose ]]; then
    cat >/dev/null
  elif [[ $2 == gamecenter-shinomiya-unity-web ]]; then
    cat "$stage/unity-before.json"
  else
    cat "$stage/expected-targets.json"
  fi
}
curl() { printf '%s\\n' "${!#}" >>"$stage/health-requests"; }
'''
            result = subprocess.run(['bash', '-s'], input=setup + tail, cwd=root,
                                    env={**os.environ, 'TEST_STAGE': str(stage), 'TEST_SHA': sha},
                                    text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Classic/gateway release ' + sha, result.stdout)
            self.assertEqual((stage / 'health-requests').read_text().splitlines(), [
                'http://127.0.0.1:18094/01/api/status', 'http://127.0.0.1:18094/02/healthz'])
            self.assertEqual(release.read_text(), original +
                             'CLASSIC_RELEASE_TAG=' + sha + '\nGATEWAY_RELEASE_TAG=' + sha + '\n')
            self.assertEqual(release.stat().st_mode & 0o777, 0o640)

if __name__=='__main__':unittest.main()
