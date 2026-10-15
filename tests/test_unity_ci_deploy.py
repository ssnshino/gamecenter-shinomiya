"""CI wrapper contract; never connects to BASE or invokes Docker."""
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

REPO = pathlib.Path(__file__).parents[1]
SHA, UNITY = 'a' * 40, 'b' * 40
ROOT = '/home/shino/source/repos/upstream/gamecenter-shinomiya'
RECEIPT = ROOT + '/runtime/deploy/unity-colony-' + SHA + '-20261015T120000Z'
spec = importlib.util.spec_from_file_location('guard', REPO / 'scripts/check-unity-web-release.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class ScopeTests(unittest.TestCase):
    def test_only_unity_workflow_is_added_to_the_deploy_scope(self):
        def git_result(args, cwd=None):
            if args[1:3] == ['branch', '--show-current']: return 'dev\n'
            if args[1:3] == ['remote', 'get-url']: return 'https://github.com/ssnshino/gamecenter-shinomiya.git\n'
            if args[1:3] == ['diff', '--name-only']: return self.changed + '\n'
            return ''
        with patch.object(guard, 'run', side_effect=git_result):
            self.changed = '.github/workflows/deploy-unity-web.yml'
            guard.check_scope(ROOT, 'c' * 40, SHA)
            self.changed = '.github/workflows/build-classic-gateway.yml'
            with self.assertRaisesRegex(ValueError, 'Out-of-scope'):
                guard.check_scope(ROOT, 'c' * 40, SHA)

    def test_prs_cannot_enter_the_secret_using_job(self):
        workflow = (REPO / '.github/workflows/deploy-unity-web.yml').read_text()
        self.assertIn("if: github.event_name != 'pull_request' && github.ref == 'refs/heads/dev'", workflow)
        self.assertIn('steps.accept.outcome !=', workflow)
        self.assertNotIn('pull_request_target', workflow)
        self.assertNotIn('deploy-classic-gateway.sh', workflow)


@unittest.skipUnless(os.name == 'posix' and shutil.which('bash'), 'SSH wrapper harness runs in Linux CI')
class WrapperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        for name in ['ci-deploy-unity-web.sh', 'check-unity-web-release.py']:
            shutil.copyfile(REPO / 'scripts' / name, self.root / 'scripts' / name)
        (self.root / 'docs/head').mkdir(parents=True)
        (self.root / 'docs/head/UNITY_ARTIFACT_MANIFEST.json').write_text(json.dumps({'games': [{'game': 'colony-racer', 'unitySourceSha': UNITY}]}))
        self.bin = self.root / 'bin'; self.bin.mkdir()
        fake = self.bin / 'ssh'
        fake.write_text('''#!/usr/bin/env bash
set -euo pipefail
key=''
while (( $# )); do if [[ $1 == -i ]]; then key=$2; shift; fi; shift; done
python3 - "$key" <<'PY'
import os,pathlib,sys
p=pathlib.Path(sys.argv[1]);assert p.stat().st_mode&0o777==0o600
assert 'DEV_DEPLOY_SSH_KEY' not in os.environ
pathlib.Path('key-path.txt').write_text(str(p))
PY
cat > remote-input.txt
printf 'Provisional public Unity release. Receipt: %s/runtime/deploy/unity-colony-%s-20261015T120000Z\\n' "$DEV_DEPLOY_REPO_PATH" "$SOURCE_SHA"
''')
        fake.chmod(0o755)
        self.env = os.environ | {'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
            'SOURCE_SHA': SHA, 'DEV_DEPLOY_REPO_PATH': ROOT, 'DEV_DEPLOY_HOST': 'example.invalid',
            'DEV_DEPLOY_PORT': '4523', 'DEV_DEPLOY_SSH_KEY': 'FAKE_KEY_NOT_A_REAL_CREDENTIAL',
            'DEV_DEPLOY_KNOWN_HOSTS': 'fake-public-host-key', 'GITHUB_OUTPUT': str(self.root / 'output.txt')}

    def call(self, *args, env=None):
        return subprocess.run(['bash', 'scripts/ci-deploy-unity-web.sh', *args], cwd=self.root,
            env=self.env | (env or {}), text=True, capture_output=True, timeout=15)

    def test_provision_uses_stdin_and_removes_the_ephemeral_key(self):
        result = self.call('deploy')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('receipt=' + RECEIPT, (self.root / 'output.txt').read_text())
        remote = (self.root / 'remote-input.txt').read_text()
        self.assertIn('git show "$sha:scripts/deploy-unity-web.sh"', remote)
        self.assertIn('deploy "$sha" </dev/null', remote)
        self.assertIn('timeout 1800 git fetch --progress origin dev </dev/null', remote)
        self.assertNotIn('FAKE_KEY', remote + result.stdout + result.stderr)
        self.assertFalse(pathlib.Path((self.root / 'key-path.txt').read_text()).exists())

    def test_invalid_target_and_receipts_never_invoke_ssh(self):
        for env in [{'SOURCE_SHA': 'main'}, {'DEV_DEPLOY_HOST': 'host;touch bad'}, {'DEV_DEPLOY_PORT': '0'}, {'DEV_DEPLOY_REPO_PATH': '/tmp/wrong'}]:
            with self.subTest(env=env): self.assertNotEqual(self.call('deploy', env=env).returncode, 0)
        self.assertNotEqual(self.call('rollback', RECEIPT.replace(SHA, 'c' * 40)).returncode, 0)
        self.assertNotEqual(self.call('rollback', RECEIPT + '/../other').returncode, 0)
        self.assertFalse((self.root / 'remote-input.txt').exists())

    def test_incomplete_browser_report_cannot_finalize(self):
        p = self.root / 'browser.json'; p.write_text(json.dumps({'pass': True, 'complete': False}))
        self.assertNotEqual(self.call('finalize', RECEIPT, str(p)).returncode, 0)
        self.assertFalse((self.root / 'remote-input.txt').exists())

    def test_complete_observations_are_checked_before_transfer(self):
        p = self.root / 'browser.json'
        p.write_text(json.dumps({'pass': True, 'complete': True, 'distributionSha': SHA, 'unitySourceSha': UNITY,
            'url': 'https://unity-games.wos.ktsys.jp/02/colony-racer/', 'observations': [
                {'name': name, 'pass': True, 'observedUtc': '2026-10-15T12:00:00Z', 'tool': 'test fixture'}
                for name in ['loaded', 'accelerate', 'brake', 'steer', 'reset', 'districts']]}))
        result = self.call('finalize', RECEIPT, str(p))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('FAKE_KEY', result.stdout + result.stderr)


if __name__ == '__main__': unittest.main()
