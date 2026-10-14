"""Guards for an isolated Colony WebGL release. Snapshots never contain credentials or data bodies."""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = '/home/shino/source/repos/upstream/gamecenter-shinomiya'
PUBLIC = 'https://unity-games.wos.ktsys.jp/02/'
UNITY = '/gamecenter-shinomiya-unity-web'
TAG_KEYS = {'RELEASE_TAG', 'CLASSIC_RELEASE_TAG', 'GATEWAY_RELEASE_TAG'}
RUNTIME_NAMES = ['airrace_ghosts', 'airrace_scores', 'breakout_scores', 'dungeon_scores', 'fighting_scores', 'truckers_scores']
METADATA = ['.env.routing', 'compose.dev.yaml', 'compose.public.yaml', 'gateway/default.conf']
ALLOWED_CODE = {'scripts/deploy-unity-web.sh', 'scripts/check-unity-web-release.py', 'scripts/verify-game-delivery.mjs', 'tests/test_unity_web_release.py', 'tests/game-delivery.test.mjs'}
RECOVERABLE_PHASES = {'awaiting-browser', 'failed-preflight', 'failed-final-health', 'failed-finalize-checkout', 'failed-persist-release-tag', 'failed-copy-browser-report', 'failed-final-capture', 'failed-final-verification', 'failed-unity-update', 'failed-health', 'failed-artifact-verification', 'rollback-failed'}
RECOVERABLE_PHASES |= {'unity-update', 'health', 'artifact-verification', 'final-health', 'finalize-checkout', 'persist-release-tag', 'copy-browser-report', 'final-capture', 'final-verification', 'manual-rollback'}
RETRY_PHASES = {'rolled-back', 'rolled-back-mixed-checkout-awaiting-retry'}


def require(value, message):
    if not value:
        raise ValueError(message)


def sha_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def run(args, cwd=None):
    process = subprocess.run(args, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=120)
    require(process.returncode == 0, f'{args[0]} failed with exit {process.returncode}')
    return process.stdout


def release_values(path):
    values = {}
    for line in pathlib.Path(path).read_text().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        require('=' in line, 'Unrecognized release configuration')
        key, value = line.split('=', 1)
        require(key in TAG_KEYS and re.fullmatch('[a-f0-9]{40}', value), 'Release configuration must contain only known SHA tags')
        require(key not in values, 'Duplicate release tag')
        values[key] = value
    require(set(values) == TAG_KEYS, 'All three independent release tags are required')
    return values


def canonical_container_record(record):
    """Docker inspect order is not a mount or DNS-alias configuration change."""
    result = dict(record)
    result['mounts'] = sorted(record['mounts'], key=lambda mount: json.dumps(mount, sort_keys=True, separators=(',', ':')))
    result['networks'] = {
        name: {**network, 'aliases': sorted(network['aliases']) if isinstance(network.get('aliases'), list) else network.get('aliases')}
        for name, network in record['networks'].items()
    }
    return result


def container_record(item):
    config = item['Config']
    return canonical_container_record({
        'name': item['Name'], 'id': item['Id'], 'image': item['Image'], 'tag': config['Image'],
        'running': item['State']['Running'], 'state': item['State']['Status'],
        'startedAt': item['State']['StartedAt'], 'restarts': item['RestartCount'],
        'readonly': item['HostConfig']['ReadonlyRootfs'], 'workingDir': config['WorkingDir'], 'user': config.get('User', ''),
        'mounts': [{key: mount.get(key) for key in ['Type', 'Source', 'Destination', 'RW']} for mount in item.get('Mounts', [])],
        'labels': {key: value for key, value in config.get('Labels', {}).items() if key.startswith('com.docker.compose.')},
        'networks': {name: {'ip': net.get('IPAddress'), 'aliases': net.get('Aliases')} for name, net in item['NetworkSettings'].get('Networks', {}).items()},
    })


def capture(root, allow_unhealthy=False):
    root = pathlib.Path(root).resolve()
    require(str(root) == ROOT, 'Unexpected live repository')
    ids = run(['docker', 'ps', '-aq']).splitlines()
    items = json.loads(run(['docker', 'inspect', *ids])) if ids else []
    containers = sorted([container_record(item) for item in items], key=lambda item: item['name'])
    runtime = []
    for name in RUNTIME_NAMES:
        path = root / 'runtime/classic' / (name + '.json')
        require(path.is_file() and not path.is_symlink(), 'Missing or symbolic runtime file')
        stat = path.stat()
        value = json.loads(path.read_text())
        require(isinstance(value, (list, dict)) and stat.st_uid == 1000, 'Invalid runtime data or owner')
        runtime.append({'name': name, 'bytes': stat.st_size, 'sha256': sha_file(path), 'uid': stat.st_uid, 'gid': stat.st_gid, 'mode': stat.st_mode & 0o777})
    # Read the active image's files, not merely the checkout's expected assets.
    javascript = "const fs=require('fs'),p=require('path'),c=require('crypto');function walk(root,prefix=''){let out=[];for(const d of fs.readdirSync(p.join(root,prefix),{withFileTypes:true})){let rel=prefix?prefix+'/'+d.name:d.name;if(d.isDirectory())out.push(...walk(root,rel));else if(d.isFile()){let b=fs.readFileSync(p.join(root,rel));out.push({path:rel,bytes:b.length,sha256:c.createHash('sha256').update(b).digest('hex')});}else throw Error('Nonregular asset');}return out.sort((a,b)=>a.path<b.path?-1:a.path>b.path?1:0);}console.log(JSON.stringify(['airrace3d','colony-racer'].map(game=>({game,files:walk('/app/public/'+game)}))));"
    actual = []
    observed = True
    try:
        actual = json.loads(run(['docker', 'exec', UNITY.lstrip('/'), 'node', '-e', javascript]))
    except (ValueError, subprocess.TimeoutExpired):
        if not allow_unhealthy:
            raise
        observed = False
    return {
        'schema': 1, 'root': str(root), 'checkoutSha': run(['git', 'rev-parse', 'HEAD'], cwd=root).strip(),
        'containers': containers, 'runtime': runtime, 'actualGames': actual, 'actualGamesObserved': observed,
        'metadataHashes': {name: sha_file(root / name) for name in METADATA},
        'releaseValues': release_values(root / '.env.release'), 'releaseFileSha256': sha_file(root / '.env.release'),
        'artifactManifest': json.loads((root / 'docs/head/UNITY_ARTIFACT_MANIFEST.json').read_text()),
    }


def raw_inventory(game):
    return sorted([{key: entry[key] for key in ['path', 'bytes', 'sha256']} for entry in game['files']], key=lambda entry: entry['path'])


def game(items, name):
    return next(item for item in items if item['game'] == name)


def assets_match(actual, manifest):
    for name in ['airrace3d', 'colony-racer']:
        require(raw_inventory(game(actual, name)) == raw_inventory(game(manifest['games'], name)), f'Active {name} files do not match the manifest')


def preserved_assets(before, proposed):
    require(raw_inventory(game(before['actualGames'], 'airrace3d')) == raw_inventory(game(proposed['games'], 'airrace3d')), 'AirRace bytes changed')
    previous = raw_inventory(game(before['actualGames'], 'colony-racer'))
    current = {entry['path']: entry for entry in raw_inventory(game(proposed['games'], 'colony-racer'))}
    for entry in previous:
        if entry['path'].startswith('StreamingAssets/'):
            require(current.get(entry['path']) == entry, 'Existing Colony catalog/Bundle changed: ' + entry['path'])
    colony = game(proposed['games'], 'colony-racer')
    require(colony.get('unityBuildPerformed') is True and re.fullmatch('[a-f0-9]{40}', colony.get('unitySourceSha', '')), 'Missing explicit Colony build provenance')


def check_scope(root, previous, requested):
    require(re.fullmatch('[a-f0-9]{40}', requested) and re.fullmatch('[a-f0-9]{40}', previous), 'Exact commits are required')
    require(run(['git', 'branch', '--show-current'], cwd=root).strip() == 'dev', 'Live checkout must be dev')
    require(not run(['git', 'status', '--porcelain', '--untracked-files=normal'], cwd=root).strip(), 'Dirty live checkout')
    require(run(['git', 'remote', 'get-url', 'origin'], cwd=root).strip() in ['https://github.com/ssnshino/gamecenter-shinomiya.git', 'https://github.com/ssnshino/gamecenter-shinomiya', 'git@github.com:ssnshino/gamecenter-shinomiya.git'], 'Unexpected origin')
    run(['git', 'merge-base', '--is-ancestor', previous, requested], cwd=root)
    paths = run(['git', 'diff', '--name-only', previous, requested], cwd=root).splitlines()
    for name in paths:
        documentation = name in ['README.md', 'AGENTS.md'] or name.startswith(('docs/', 'plan/', 'snapshot/'))
        require(documentation or name in ALLOWED_CODE or name.startswith('apps/unity-web/public/colony-racer/'), 'Out-of-scope source change: ' + name)


def preflight(before, proposed):
    assets_match(before['actualGames'], before['artifactManifest'])
    preserved_assets(before, proposed)
    records = {item['name']: item for item in before['containers']}
    for name in ['classic', 'unity-web', 'gateway']:
        item = records['/gamecenter-shinomiya-' + name]
        require(item['running'] and item['labels'].get('com.docker.compose.project') == 'gamecenter-shinomiya', 'Unexpected service state or project')
        require(item['labels'].get('com.docker.compose.project.working_dir') == ROOT, 'Unexpected live Compose mapping')
    unity = records[UNITY]
    require(unity['readonly'] and not unity['mounts'] and unity['workingDir'] == '/app', 'Unexpected Unity filesystem mapping')
    classic = records['/gamecenter-shinomiya-classic']
    require(classic.get('user') == '1000:1000', 'Unexpected classic runtime user')
    require(classic['mounts'] == [{'Type': 'bind', 'Source': ROOT + '/runtime/classic', 'Destination': '/data', 'RW': True}], 'Active classic runtime bind differs')
    values = before['releaseValues']
    for service, key in [('classic', 'CLASSIC_RELEASE_TAG'), ('gateway', 'GATEWAY_RELEASE_TAG'), ('unity-web', 'RELEASE_TAG')]:
        require(records['/gamecenter-shinomiya-' + service]['tag'] == 'gamecenter-shinomiya-' + service + ':' + values[key], 'Release tag disagrees with the active image')
    return True


def check_compose(root, before, requested):
    command = ['docker', 'compose', '--project-directory', root, '--env-file', root + '/.env.release', '--env-file', root + '/.env.routing', '-f', root + '/compose.dev.yaml', '-f', root + '/compose.public.yaml', 'config', '--format', 'json']
    config = json.loads(run(command))
    require(config['name'] == 'gamecenter-shinomiya', 'Unexpected effective Compose project')
    services = config['services']
    require(set(services) == {'classic', 'unity-web', 'gateway'}, 'Unexpected effective services')
    records = {item['name']: item for item in before['containers']}
    for name, service in services.items():
        expected = 'gamecenter-shinomiya-unity-web:' + requested if name == 'unity-web' else records['/gamecenter-shinomiya-' + name]['tag']
        require(service['image'] == expected and service['container_name'] == 'gamecenter-shinomiya-' + name, 'Unexpected effective image or container')
        require(not any(service.get(key) for key in ['privileged', 'devices', 'cap_add', 'network_mode', 'pid', 'ipc']), 'Unexpected elevated service settings')
    classic = services['classic']
    require(classic['read_only'] and services['unity-web']['read_only'], 'Read-only application filesystems are required')
    volumes = classic['volumes']
    require(len(volumes) == 1 and volumes[0]['type'] == 'bind' and volumes[0]['source'] == root + '/runtime/classic' and volumes[0]['target'] == '/data', 'Unexpected runtime data mapping')
    require(not services['unity-web'].get('volumes') and not services['gateway'].get('volumes'), 'Unexpected application mounts')
    require(not classic.get('ports') and not services['unity-web'].get('ports'), 'Unexpected public application port')
    ports = services['gateway']['ports']
    require(len(ports) == 1 and ports[0]['host_ip'] == '127.0.0.1' and str(ports[0]['published']) == '18094' and str(ports[0]['target']) == '80', 'Unexpected gateway port')
    require(set(classic['networks']) == set(services['unity-web']['networks']) == {'internal'}, 'Unexpected application networks')
    require(set(services['gateway']['networks']) == {'internal', 'wos-proxy-network'}, 'Unexpected gateway networks')


def check_preservation(before, after, proposed, requested, mode):
    require(mode in ['provisional', 'finalized', 'rollback'], 'Unknown verification mode')
    def others(snapshot):
        return [item for item in snapshot['containers'] if item['name'] != UNITY]
    require(others(before) == others(after), 'An unrelated container changed')
    require(before['runtime'] == after['runtime'], 'Runtime data or ownership changed')
    require(before['metadataHashes'] == after['metadataHashes'], 'Compose, routing or gateway configuration changed')
    old = next(item for item in before['containers'] if item['name'] == UNITY)
    new = next(item for item in after['containers'] if item['name'] == UNITY)
    require(new['running'] and new['readonly'] and not new['mounts'] and new['workingDir'] == old['workingDir'], 'Unexpected Unity runtime mapping')
    require(set(new['networks']) == set(old['networks']), 'Unity network membership changed')
    for name in old['networks']:
        require(new['networks'][name]['aliases'] == old['networks'][name]['aliases'], 'Unity network aliases changed')
    expected_tags = dict(before['releaseValues'])
    if mode == 'finalized':
        expected_tags['RELEASE_TAG'] = requested
        require(after['checkoutSha'] == requested, 'Finalized checkout SHA differs')
    elif mode == 'rollback':
        require(after['checkoutSha'] in {before['checkoutSha'], requested}, 'Rollback checkout is not a known release commit')
        require(after['releaseFileSha256'] == before['releaseFileSha256'], 'Rollback release configuration differs from the backup')
    else:
        require(after['checkoutSha'] == before['checkoutSha'], 'Checkout moved before acceptance')
        require(after['releaseFileSha256'] == before['releaseFileSha256'], 'Release settings changed before acceptance')
    require(after['releaseValues'] == expected_tags, 'Unexpected release configuration change')
    if mode == 'rollback':
        require(new['tag'] == old['tag'] and new['image'] == old['image'], 'Rollback did not restore the old Unity image')
        assets_match(after['actualGames'], before.get('servedArtifactManifest', before['artifactManifest']))
    else:
        require(new['tag'] == 'gamecenter-shinomiya-unity-web:' + requested, 'Active Unity release tag differs')
        assets_match(after['actualGames'], proposed)
        preserved_assets(before, proposed)
    return True


def receipt_action(receipt, action):
    phase = receipt.get('phase')
    allowed = {'finalize': {'awaiting-browser'}, 'rollback': RECOVERABLE_PHASES | RETRY_PHASES, 'retry': RETRY_PHASES}
    require(action in allowed and phase in allowed[action], f'Receipt phase {phase} does not allow {action}')
    require(re.fullmatch('[a-f0-9]{40}', receipt.get('requestedSha', '')), 'Receipt has no exact requested commit')
    require(receipt.get('publicBase') == PUBLIC, 'Receipt refers to another public service')


def known_release_hashes(before, requested, backup):
    require(hashlib.sha256(backup.encode()).hexdigest() == before['releaseFileSha256'], 'Release backup hash differs')
    lines = backup.splitlines()
    next_text = '\n'.join('RELEASE_TAG=' + requested if line.startswith('RELEASE_TAG=') else line for line in lines) + '\n'
    return {before['releaseFileSha256'], hashlib.sha256(next_text.encode()).hexdigest()}


def recovery_preflight(before, current, proposed, requested, built_image, backup):
    require(current['checkoutSha'] in {before['checkoutSha'], requested}, 'Recovery checkout is not a known release commit')
    require(current['metadataHashes'] == before['metadataHashes'], 'Recovery routing or Compose changed')
    require(current['runtime'] == before['runtime'], 'Recovery runtime data changed; do not restore data')
    def others(snapshot):
        return [item for item in snapshot['containers'] if item['name'] != UNITY]
    require(others(current) == others(before), 'Recovery unrelated service changed')
    old = next(item for item in before['containers'] if item['name'] == UNITY)
    active = next(item for item in current['containers'] if item['name'] == UNITY)
    known_images = {(old['tag'], old['image']), ('gamecenter-shinomiya-unity-web:' + requested, built_image)}
    require((active['tag'], active['image']) in known_images, 'Recovery image/tag is not a known immutable release')
    require(active['readonly'] and not active['mounts'] and active['workingDir'] == old['workingDir'], 'Recovery Unity filesystem mapping changed')
    require(set(active['networks']) == set(old['networks']), 'Recovery Unity network changed')
    require(all(set(active['networks'][name]['aliases']) == set(old['networks'][name]['aliases']) for name in old['networks']), 'Recovery Unity aliases changed')
    tags = current['releaseValues']
    require(tags['RELEASE_TAG'] in {before['releaseValues']['RELEASE_TAG'], requested}, 'Recovery Unity release tag is unknown')
    require(all(tags[key] == before['releaseValues'][key] for key in TAG_KEYS - {'RELEASE_TAG'}), 'Recovery other release tags changed')
    require(current['releaseFileSha256'] in known_release_hashes(before, requested, backup), 'Recovery environment contains concurrent edits')
    if current.get('actualGamesObserved', True):
        expected = before['artifactManifest'] if active['image'] == old['image'] else proposed
        assets_match(current['actualGames'], expected)
    # An unhealthy Unity process cannot inventory assets. Recovery is still
    # bounded by its exact Docker image ID; this is explicitly unobserved.
    return True


def prepare_retry(before, current, proposed, requested, built_image, backup):
    recovery_preflight(before, current, proposed, requested, built_image, backup)
    old = next(item for item in before['containers'] if item['name'] == UNITY)
    active = next(item for item in current['containers'] if item['name'] == UNITY)
    require(active['running'] and (active['tag'], active['image']) == (old['tag'], old['image']), 'Retry requires the restored old image')
    require(current.get('actualGamesObserved', True), 'Retry requires an actual restored asset inventory')
    require(current['releaseValues'] == before['releaseValues'] and current['releaseFileSha256'] == before['releaseFileSha256'], 'Retry requires restored release settings')
    assets_match(current['actualGames'], before['artifactManifest'])
    result = dict(current)
    result['servedArtifactManifest'] = before['artifactManifest']
    result['servedManifestReference'] = {'snapshot': 'before.json', 'image': old['image'], 'tag': old['tag'], 'checkoutSha': before['checkoutSha']}
    # Keep the real current checkout manifest and SHA. The separate reference
    # documents why they can differ after a bounded rollback.
    return result


def recovered_phase(before, after, receipt):
    result = dict(receipt)
    mixed = after['checkoutSha'] != before['checkoutSha']
    result.update(phase='rolled-back-mixed-checkout-awaiting-retry' if mixed else 'rolled-back', checkoutSha=after['checkoutSha'], mixedCheckout=mixed, adoptionComplete=False, retryRequired=True)
    return result


def restore_release(root, before, current, requested, backup):
    path = pathlib.Path(root) / '.env.release'
    require(sha_file(path) == current['releaseFileSha256'] and release_values(path) == current['releaseValues'], 'Release settings changed during recovery')
    require(sha_file(path) in known_release_hashes(before, requested, backup), 'Unknown release settings cannot be restored')
    if sha_file(path) == before['releaseFileSha256']:
        return
    atomic_write(path, backup, path.stat().st_mode & 0o777)


def check_browser(report, requested, proposed):
    require(report.get('complete') is True and report.get('pass') is True, 'Browser acceptance is incomplete')
    require(report.get('distributionSha') == requested and report.get('unitySourceSha') == game(proposed['games'], 'colony-racer')['unitySourceSha'], 'Browser acceptance refers to different source')
    require(report.get('url') == PUBLIC + 'colony-racer/', 'Unexpected accepted URL')
    observations = report.get('observations', [])
    needed = {'loaded', 'accelerate', 'brake', 'steer', 'reset', 'districts'}
    require(needed.issubset({item.get('name') for item in observations if item.get('pass') is True and item.get('observedUtc') and item.get('tool')}), 'Missing real browser observations')


def check_image(snapshot, expected):
    item = next(item for item in snapshot['containers'] if item['name'] == UNITY)
    require(item['image'] == expected, 'Active Unity image differs from the built image')


def same_unity(first, second):
    a = next(item for item in first['containers'] if item['name'] == UNITY)
    b = next(item for item in second['containers'] if item['name'] == UNITY)
    require(a == b, 'Unity changed after the accepted browser observation')


def persist_release(root, before, requested):
    path = pathlib.Path(root) / '.env.release'
    require(sha_file(path) == before['releaseFileSha256'] and release_values(path) == before['releaseValues'], 'Release settings changed concurrently')
    lines = path.read_text().splitlines()
    lines = [('RELEASE_TAG=' + requested) if line.startswith('RELEASE_TAG=') else line for line in lines]
    atomic_write(path, '\n'.join(lines) + '\n', path.stat().st_mode & 0o777)


def backup_release(root, before, destination):
    source = pathlib.Path(root) / '.env.release'
    require(sha_file(source) == before['releaseFileSha256'] and release_values(source) == before['releaseValues'], 'Release settings changed before backup')
    # This deployment has three public SHA tag lines. Do not archive arbitrary
    # environment entries or comments that could contain credentials.
    text = source.read_text()
    require(all(not line.strip() or line.split('=', 1)[0] in TAG_KEYS for line in text.splitlines()), 'Release backup contains unknown content')
    require(not pathlib.Path(destination).exists(), 'Release backup already exists')
    atomic_write(destination, text, source.stat().st_mode & 0o777)


def atomic_write(path, text, mode=None):
    path = pathlib.Path(path)
    if mode is None:
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    descriptor, name = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    temporary = pathlib.Path(name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, 'w') as output:
            descriptor = None
            output.write(text)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
        parent = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(parent)
        finally:
            os.close(parent)
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()


def write_json(path, value):
    atomic_write(path, json.dumps(value, indent=2) + '\n')


def record_receipt(path, phase, exit_code=None):
    data = json.loads(pathlib.Path(path).read_text()) if pathlib.Path(path).exists() else {}
    data.update(phase=phase, adoptionComplete=phase == 'accepted')
    if phase in {'accepted', 'awaiting-browser'}:
        data.update(retryRequired=False, mixedCheckout=False)
    if exit_code is not None:
        data['exitCode'] = exit_code
    write_json(path, data)


if __name__ == '__main__':
    command, *args = sys.argv[1:]
    if command == 'capture':
        write_json(args[1], capture(args[0], len(args) > 2 and args[2] == '--allow-unhealthy-unity'))
    elif command == 'scope':
        check_scope(*args)
    elif command == 'preflight':
        preflight(*[json.load(open(path)) for path in args])
    elif command == 'compose':
        check_compose(args[0], json.load(open(args[1])), args[2])
    elif command == 'verify':
        before, after, proposed = [json.load(open(path)) for path in args[:3]]
        check_preservation(before, after, proposed, args[3], args[4])
    elif command == 'browser':
        check_browser(json.load(open(args[0])), args[1], json.load(open(args[2])))
    elif command == 'image':
        check_image(json.load(open(args[0])), pathlib.Path(args[1]).read_text().strip())
    elif command == 'same-unity':
        same_unity(*[json.load(open(path)) for path in args])
    elif command == 'persist':
        persist_release(args[0], json.load(open(args[1])), args[2])
    elif command == 'backup-release':
        backup_release(args[0], json.load(open(args[1])), args[2])
    elif command == 'receipt-action':
        receipt_action(json.load(open(args[0])), args[1])
    elif command in {'recovery-preflight', 'prepare-retry'}:
        before, current, proposed = [json.load(open(path)) for path in args[:3]]
        built = pathlib.Path(args[4]).read_text().strip()
        backup = pathlib.Path(args[5]).read_text()
        if command == 'prepare-retry':
            write_json(args[6], prepare_retry(before, current, proposed, args[3], built, backup))
        else:
            recovery_preflight(before, current, proposed, args[3], built, backup)
    elif command == 'restore-release':
        restore_release(args[0], json.load(open(args[1])), json.load(open(args[2])), args[3], pathlib.Path(args[4]).read_text())
    elif command == 'recovered-receipt':
        before, after, receipt = [json.load(open(path)) for path in args]
        write_json(args[2], recovered_phase(before, after, receipt))
    elif command == 'same-checkout':
        first, second = [json.load(open(path)) for path in args]
        require(first['checkoutSha'] == second['checkoutSha'], 'Checkout changed during image recovery')
    elif command == 'receipt':
        path, phase, *extra = args
        record_receipt(path, phase, int(extra[0]) if extra else None)
    else:
        raise ValueError('Unknown guard command')
