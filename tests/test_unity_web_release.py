"""Release guards run on in-memory fixtures; these tests cannot invoke Docker or SSH."""
import copy
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('unity_release', pathlib.Path(__file__).parents[1] / 'scripts/check-unity-web-release.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
OLD, NEW, UNITY_SOURCE = 'a' * 40, 'b' * 40, 'c' * 40
BACKUP = f'RELEASE_TAG={OLD}\nCLASSIC_RELEASE_TAG={OLD}\nGATEWAY_RELEASE_TAG={OLD}\n'


def fixture():
    def asset(path, digest):
        return {'path': path, 'bytes': 10, 'sha256': digest * 64, 'httpSha256': digest * 64}
    games = [{'game': 'airrace3d', 'files': [asset('Build/a.wasm.gz', 'a')]}, {'game': 'colony-racer', 'files': [asset('Build/a.wasm.gz', 'b'), asset('StreamingAssets/AirRace/round_world_catalog.json', 'c')]}]
    manifest = {'schema': 1, 'sourceSha': OLD, 'games': games}
    containers = []
    for name in ['classic', 'unity-web', 'gateway', 'unrelated']:
        containers.append({'name': '/gamecenter-shinomiya-' + name, 'id': name, 'image': 'old-' + name, 'tag': 'gamecenter-shinomiya-' + name + ':' + OLD, 'running': True, 'state': 'running', 'startedAt': 'start', 'restarts': 0, 'readonly': name != 'gateway', 'workingDir': '/app' if name == 'unity-web' else '/', 'mounts': [], 'labels': {'com.docker.compose.project': 'gamecenter-shinomiya', 'com.docker.compose.project.working_dir': guard.ROOT}, 'networks': {'internal': {'ip': '192.168.1.2', 'aliases': [name]}}})
    before = {'checkoutSha': OLD, 'containers': containers, 'runtime': [{'name': 'scores', 'sha256': 'a' * 64}], 'metadataHashes': {'routing': 'a' * 64}, 'releaseValues': {'RELEASE_TAG': OLD, 'CLASSIC_RELEASE_TAG': OLD, 'GATEWAY_RELEASE_TAG': OLD}, 'releaseFileSha256': hashlib.sha256(BACKUP.encode()).hexdigest(), 'actualGames': copy.deepcopy(games), 'artifactManifest': manifest}
    containers[0]['user'] = '1000:1000'
    containers[0]['mounts'] = [{'Type': 'bind', 'Source': guard.ROOT + '/runtime/classic', 'Destination': '/data', 'RW': True}]
    proposed = copy.deepcopy(manifest)
    proposed['games'][1].update(unitySourceSha=UNITY_SOURCE, unityBuildPerformed=True)
    proposed['games'][1]['files'][0] = asset('Build/new.wasm.gz', 'd')
    after = copy.deepcopy(before)
    unity = next(item for item in after['containers'] if item['name'] == guard.UNITY)
    unity.update(id='new-unity', image='new-image', tag='gamecenter-shinomiya-unity-web:' + NEW, startedAt='new-start')
    unity['networks']['internal']['ip'] = '192.168.1.9'
    after['actualGames'] = copy.deepcopy(proposed['games'])
    return before, after, proposed


class ReleaseGuardTests(unittest.TestCase):
    def test_provisional_preserves_other_services_data_tags_and_airrace(self):
        before, after, proposed = fixture()
        self.assertTrue(guard.preflight(before, proposed))
        self.assertTrue(guard.check_preservation(before, after, proposed, NEW, 'provisional'))

    def test_finalization_allows_only_unity_tag_and_exact_checkout(self):
        before, after, proposed = fixture()
        after['checkoutSha'] = NEW
        after['releaseValues']['RELEASE_TAG'] = NEW
        self.assertTrue(guard.check_preservation(before, after, proposed, NEW, 'finalized'))
        after['releaseValues']['GATEWAY_RELEASE_TAG'] = NEW
        with self.assertRaisesRegex(ValueError, 'configuration'):
            guard.check_preservation(before, after, proposed, NEW, 'finalized')

    def test_unrelated_container_and_runtime_drift_fail_closed(self):
        for category in ['container', 'runtime', 'routing']:
            before, after, proposed = fixture()
            if category == 'container': after['containers'][0]['id'] = 'changed'
            if category == 'runtime': after['runtime'][0]['sha256'] = 'b' * 64
            if category == 'routing': after['metadataHashes']['routing'] = 'b' * 64
            with self.assertRaises(ValueError): guard.check_preservation(before, after, proposed, NEW, 'provisional')

    def test_wrong_actual_classic_bind_is_rejected(self):
        before, _, proposed = fixture()
        before['containers'][0]['mounts'][0]['Source'] = '/wrong-data'
        with self.assertRaisesRegex(ValueError, 'runtime bind'): guard.preflight(before, proposed)

    def test_airrace_and_existing_colony_bundle_changes_are_rejected(self):
        for game_index, file_index in [(0, 0), (1, 1)]:
            before, _, proposed = fixture()
            proposed['games'][game_index]['files'][file_index]['sha256'] = 'f' * 64
            with self.assertRaises(ValueError): guard.preserved_assets(before, proposed)

    def test_provisional_release_cannot_change_env_or_checkout(self):
        for field in ['checkoutSha', 'releaseFileSha256']:
            before, after, proposed = fixture()
            after[field] = 'changed'
            with self.assertRaises(ValueError): guard.check_preservation(before, after, proposed, NEW, 'provisional')

    def test_rollback_requires_actual_old_image_and_old_assets(self):
        before, _, proposed = fixture()
        restored = copy.deepcopy(before)
        self.assertTrue(guard.check_preservation(before, restored, proposed, NEW, 'rollback'))
        restored['containers'][1]['image'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'Rollback'): guard.check_preservation(before, restored, proposed, NEW, 'rollback')

    def test_missing_provenance_is_not_inferred(self):
        before, _, proposed = fixture()
        proposed['games'][1]['unityBuildPerformed'] = False
        with self.assertRaisesRegex(ValueError, 'provenance'): guard.preserved_assets(before, proposed)

    def test_changed_unity_after_browser_and_retagged_image_are_rejected(self):
        _, after, _ = fixture()
        guard.check_image(after, 'new-image')
        with self.assertRaisesRegex(ValueError, 'built image'): guard.check_image(after, 'another-image')
        changed = copy.deepcopy(after)
        next(item for item in changed['containers'] if item['name'] == guard.UNITY)['id'] = 'another-container'
        with self.assertRaisesRegex(ValueError, 'browser observation'): guard.same_unity(after, changed)

    def test_browser_needs_real_observations_and_matching_source_and_url(self):
        _, _, proposed = fixture()
        report = {'complete': True, 'pass': True, 'distributionSha': NEW, 'unitySourceSha': UNITY_SOURCE, 'url': guard.PUBLIC + 'colony-racer/', 'observations': [{'name': name, 'pass': True, 'observedUtc': '2026-10-14T13:00:00Z', 'tool': 'browser'} for name in ['loaded', 'accelerate', 'brake', 'steer', 'reset', 'districts']]}
        guard.check_browser(report, NEW, proposed)
        for field, value in [('url', 'http://localhost/'), ('unitySourceSha', OLD), ('observations', [])]:
            bad = copy.deepcopy(report); bad[field] = value
            with self.assertRaises(ValueError): guard.check_browser(bad, NEW, proposed)

    def test_secret_environment_is_never_snapshot(self):
        source = {'Name': '/game', 'Id': 'id', 'Image': 'image', 'Config': {'Image': 'tag', 'WorkingDir': '/', 'Env': ['PASSWORD=secret-value'], 'Labels': {}}, 'State': {'Running': True, 'Status': 'running', 'StartedAt': 'start'}, 'RestartCount': 0, 'HostConfig': {'ReadonlyRootfs': True}, 'NetworkSettings': {'Networks': {}}, 'Mounts': []}
        self.assertNotIn('secret-value', json.dumps(guard.container_record(source)))

    def test_inspect_mount_and_alias_order_is_canonical_without_losing_fields(self):
        source = {'Name': '/game', 'Id': 'id', 'Image': 'image', 'Config': {'Image': 'tag', 'WorkingDir': '/', 'Labels': {}}, 'State': {'Running': True, 'Status': 'running', 'StartedAt': 'start'}, 'RestartCount': 0, 'HostConfig': {'ReadonlyRootfs': True}, 'NetworkSettings': {'Networks': {'internal': {'IPAddress': '192.168.1.2', 'Aliases': ['z', 'a', 'a']}, 'other': {'IPAddress': '192.168.2.2', 'Aliases': None}}}, 'Mounts': [{'Type': 'bind', 'Source': '/first', 'Destination': '/a', 'RW': True}, {'Type': 'volume', 'Source': '/second', 'Destination': '/b', 'RW': False}]}
        reversed_source = copy.deepcopy(source)
        reversed_source['Mounts'].reverse()
        reversed_source['NetworkSettings']['Networks']['internal']['Aliases'].reverse()
        first, second = [guard.container_record(value) for value in [source, reversed_source]]
        self.assertEqual(first, second)
        self.assertEqual(first['networks']['internal']['aliases'], ['a', 'a', 'z'])
        self.assertIsNone(first['networks']['other']['aliases'])
        self.assertEqual(source['NetworkSettings']['Networks']['internal']['Aliases'], ['z', 'a', 'a'])
        self.assertEqual(len(first['mounts']), 2)
        for change in ['add', 'remove', 'rw', 'source', 'destination']:
            changed = copy.deepcopy(source)
            if change == 'add': changed['Mounts'].append({'Type': 'bind', 'Source': '/extra', 'Destination': '/c', 'RW': True})
            if change == 'remove': changed['Mounts'].pop()
            if change == 'rw': changed['Mounts'][0]['RW'] = False
            if change == 'source': changed['Mounts'][0]['Source'] = '/different'
            if change == 'destination': changed['Mounts'][0]['Destination'] = '/different'
            with self.subTest(change=change): self.assertNotEqual(first, guard.container_record(changed))

    def test_normalized_inspect_order_passes_guard_but_actual_mount_changes_fail(self):
        before, after, proposed = fixture()
        extra_mount = {'Type': 'bind', 'Source': '/extra', 'Destination': '/extra', 'RW': False}
        before['containers'][0]['mounts'].append(extra_mount)
        after['containers'][0]['mounts'].insert(0, copy.deepcopy(extra_mount))
        for snapshot in [before, after]:
            snapshot['containers'] = [guard.canonical_container_record(record) for record in snapshot['containers']]
        self.assertTrue(guard.check_preservation(before, after, proposed, NEW, 'provisional'))
        for change in ['add', 'remove', 'rw']:
            changed = copy.deepcopy(after)
            if change == 'add': changed['containers'][0]['mounts'].append({'Type': 'bind', 'Source': '/another', 'Destination': '/another', 'RW': True})
            if change == 'remove': changed['containers'][0]['mounts'].pop()
            if change == 'rw': changed['containers'][0]['mounts'][0]['RW'] = not changed['containers'][0]['mounts'][0]['RW']
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, 'unrelated container'):
                guard.check_preservation(before, changed, proposed, NEW, 'provisional')

    def test_release_file_rejects_unknown_key_and_persists_only_unity(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / '.env.release'
            original = f'RELEASE_TAG={OLD}\nCLASSIC_RELEASE_TAG={OLD}\nGATEWAY_RELEASE_TAG={OLD}\n'
            path.write_text(original)
            before = {'releaseFileSha256': guard.sha_file(path), 'releaseValues': guard.release_values(path)}
            guard.persist_release(directory, before, NEW)
            self.assertEqual(path.read_text(), original.replace('RELEASE_TAG=' + OLD + '\n', 'RELEASE_TAG=' + NEW + '\n', 1))
            path.write_text(original + 'PASSWORD=secret\n')
            with self.assertRaisesRegex(ValueError, 'only known SHA tags'): guard.release_values(path)

    def test_durable_recovery_before_merge_after_merge_and_after_persist(self):
        scenarios = [('failed-finalize-checkout', False, False), ('failed-persist-release-tag', True, False), ('failed-final-verification', True, True)]
        for phase, merged, persisted in scenarios:
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as directory:
                before, failed, proposed = fixture()
                if merged:
                    failed['checkoutSha'] = NEW
                    failed['artifactManifest'] = copy.deepcopy(proposed)
                text = BACKUP.replace('RELEASE_TAG=' + OLD + '\n', 'RELEASE_TAG=' + NEW + '\n', 1) if persisted else BACKUP
                failed['releaseFileSha256'] = hashlib.sha256(text.encode()).hexdigest()
                if persisted: failed['releaseValues']['RELEASE_TAG'] = NEW
                report_path = pathlib.Path(directory) / 'receipt.json'
                report_path.write_text(json.dumps({'phase': phase, 'requestedSha': NEW, 'previousCheckout': OLD, 'publicBase': guard.PUBLIC}))
                receipt = json.loads(report_path.read_text())
                guard.receipt_action(receipt, 'rollback')
                guard.recovery_preflight(before, failed, proposed, NEW, 'new-image', BACKUP)
                release = pathlib.Path(directory) / '.env.release'
                release.write_text(text)
                guard.restore_release(directory, before, failed, NEW, BACKUP)
                self.assertEqual(release.read_text(), BACKUP)
                restored = copy.deepcopy(failed)
                active = next(item for item in restored['containers'] if item['name'] == guard.UNITY)
                original = next(item for item in before['containers'] if item['name'] == guard.UNITY)
                active.update(image=original['image'], tag=original['tag'], id='restored-container')
                restored['actualGames'] = copy.deepcopy(before['actualGames'])
                restored['releaseValues'] = copy.deepcopy(before['releaseValues'])
                restored['releaseFileSha256'] = before['releaseFileSha256']
                guard.check_preservation(before, restored, proposed, NEW, 'rollback')
                report_path.write_text(json.dumps(guard.recovered_phase(before, restored, receipt)))
                recovered = json.loads(report_path.read_text())
                self.assertEqual(recovered['phase'], 'rolled-back-mixed-checkout-awaiting-retry' if merged else 'rolled-back')
                self.assertFalse(recovered['adoptionComplete'])
                guard.receipt_action(recovered, 'retry')
                attempt = guard.prepare_retry(before, restored, proposed, NEW, 'new-image', BACKUP)
                self.assertEqual(attempt['checkoutSha'], NEW if merged else OLD)
                self.assertEqual(attempt['artifactManifest'], proposed if merged else before['artifactManifest'])
                self.assertEqual(attempt['servedArtifactManifest'], before['artifactManifest'])
                retried = copy.deepcopy(failed)
                retried['releaseValues'] = copy.deepcopy(before['releaseValues'])
                retried['releaseFileSha256'] = before['releaseFileSha256']
                guard.check_preservation(attempt, retried, proposed, NEW, 'provisional')

    def test_recovery_refuses_unknown_checkout_tag_image_and_environment(self):
        for field in ['checkout', 'tag', 'image', 'environment']:
            before, failed, proposed = fixture()
            if field == 'checkout': failed['checkoutSha'] = 'd' * 40
            if field == 'tag': failed['releaseValues']['GATEWAY_RELEASE_TAG'] = NEW
            if field == 'image': next(item for item in failed['containers'] if item['name'] == guard.UNITY)['image'] = 'unknown-image'
            if field == 'environment': failed['releaseFileSha256'] = 'unknown-hash'
            with self.subTest(field=field), self.assertRaises(ValueError):
                guard.recovery_preflight(before, failed, proposed, NEW, 'new-image', BACKUP)

    def test_unhealthy_known_image_can_recover_but_cannot_retry_unobserved_assets(self):
        before, failed, proposed = fixture()
        failed['actualGames'] = []
        failed['actualGamesObserved'] = False
        next(item for item in failed['containers'] if item['name'] == guard.UNITY)['running'] = False
        guard.recovery_preflight(before, failed, proposed, NEW, 'new-image', BACKUP)
        with self.assertRaisesRegex(ValueError, 'restored old image'):
            guard.prepare_retry(before, failed, proposed, NEW, 'new-image', BACKUP)

    def test_receipt_phases_fail_closed_and_recovery_requires_new_browser_acceptance(self):
        receipt = {'phase': 'failed-final-verification', 'requestedSha': NEW, 'publicBase': guard.PUBLIC}
        guard.receipt_action(receipt, 'rollback')
        with self.assertRaises(ValueError): guard.receipt_action(receipt, 'finalize')
        with self.assertRaises(ValueError): guard.receipt_action(receipt, 'retry')
        receipt['phase'] = 'accepted'
        with self.assertRaises(ValueError): guard.receipt_action(receipt, 'rollback')

    def test_interrupted_in_progress_phases_allow_only_guarded_rollback(self):
        for phase in ['unity-update', 'finalize-checkout', 'persist-release-tag', 'final-verification', 'manual-rollback']:
            receipt = {'phase': phase, 'requestedSha': NEW, 'publicBase': guard.PUBLIC}
            with self.subTest(phase=phase):
                guard.receipt_action(receipt, 'rollback')
                with self.assertRaises(ValueError): guard.receipt_action(receipt, 'finalize')
                with self.assertRaises(ValueError): guard.receipt_action(receipt, 'retry')

    def test_failed_atomic_receipt_update_preserves_original_and_cleans_only_own_temp(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            receipt = root / 'receipt.json'
            guard.write_json(receipt, {'phase': 'persist-release-tag'})
            stale = root / 'receipt.json.unrelated.tmp'
            stale.write_text('preserve me')
            before = receipt.read_bytes()
            with patch.object(guard.os, 'replace', side_effect=OSError('injected replacement failure')):
                with self.assertRaises(OSError): guard.write_json(receipt, {'phase': 'accepted'})
            self.assertEqual(receipt.read_bytes(), before)
            self.assertEqual(json.loads(receipt.read_text())['phase'], 'persist-release-tag')
            self.assertEqual(stale.read_text(), 'preserve me')
            self.assertEqual(set(p.name for p in root.iterdir()), {'receipt.json', stale.name})
            guard.receipt_action({'phase': 'persist-release-tag', 'requestedSha': NEW, 'publicBase': guard.PUBLIC}, 'rollback')

    def test_release_persistence_ignores_stale_temp_and_is_retryable_after_replace_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            release = root / '.env.release'
            release.write_text(BACKUP)
            stale = root / '.env.release.unity-next'
            stale.write_text('preserve me')
            before, _, _ = fixture()
            with patch.object(guard.os, 'replace', side_effect=OSError('injected replacement failure')):
                with self.assertRaises(OSError): guard.persist_release(directory, before, NEW)
            self.assertEqual(release.read_text(), BACKUP)
            guard.persist_release(directory, before, NEW)
            self.assertEqual(guard.release_values(release)['RELEASE_TAG'], NEW)
            self.assertEqual(stale.read_text(), 'preserve me')

    def test_accepted_receipt_clears_recovery_flags_only_after_acceptance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / 'receipt.json'
            guard.write_json(path, {'phase': 'rolled-back-mixed-checkout-awaiting-retry', 'mixedCheckout': True, 'retryRequired': True, 'adoptionComplete': False})
            guard.record_receipt(path, 'awaiting-browser', 0)
            pending = json.loads(path.read_text())
            self.assertFalse(pending['adoptionComplete']);self.assertFalse(pending['mixedCheckout'])
            guard.record_receipt(path, 'accepted', 0)
            accepted = json.loads(path.read_text())
            self.assertTrue(accepted['adoptionComplete']);self.assertFalse(accepted['retryRequired'])


if __name__ == '__main__':
    unittest.main()
