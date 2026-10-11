#!/usr/bin/env bash
set -euo pipefail
[[ ${DEV_DEPLOY_ENABLED:-} == true ]] || { echo 'Deployment is disabled'; exit 1; }
[[ ${SOURCE_SHA:-} =~ ^[a-f0-9]{40}$ ]] || exit 1
[[ ${DEV_DEPLOY_HOST:-} =~ ^[a-zA-Z0-9][a-zA-Z0-9.-]*$ ]] || exit 1
[[ ${DEV_DEPLOY_PORT:-} =~ ^[0-9]+$ ]] || exit 1
(( DEV_DEPLOY_PORT > 0 && DEV_DEPLOY_PORT < 65536 )) || exit 1
[[ ${DEV_DEPLOY_REPO_PATH:-} == /home/shino/source/repos/upstream/gamecenter-shinomiya ]] || exit 1
[[ -n ${DEV_DEPLOY_SSH_KEY:-} && -n ${DEV_DEPLOY_KNOWN_HOSTS:-} ]] || exit 1
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
chmod 700 "$work"
printf '%s\n' "$DEV_DEPLOY_SSH_KEY" > "$work/key"
printf '%s\n' "$DEV_DEPLOY_KNOWN_HOSTS" > "$work/known_hosts"
chmod 600 "$work/key" "$work/known_hosts"; unset DEV_DEPLOY_SSH_KEY
ssh -i "$work/key" -p "$DEV_DEPLOY_PORT" -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$work/known_hosts" -o ConnectTimeout=20 \
 "shino@$DEV_DEPLOY_HOST" "bash -s -- '$DEV_DEPLOY_REPO_PATH' '$SOURCE_SHA'" <<'REMOTE'
set -euo pipefail
repo=$1; sha=$2; cd "$repo"
[[ $(git rev-parse --show-toplevel) == "$repo" && $(git branch --show-current) == dev ]] || exit 1
case $(git remote get-url origin) in
 https://github.com/ssnshino/gamecenter-shinomiya|https://github.com/ssnshino/gamecenter-shinomiya.git|git@github.com:ssnshino/gamecenter-shinomiya.git) ;;
 *) echo 'Unexpected origin'; exit 1;;
esac
exec 9>"$(git rev-parse --git-dir)/classic-gateway-deploy.lock"; flock -n 9 || exit 1
[[ -z $(git status --porcelain --untracked-files=normal) ]] || { echo 'Dirty checkout'; exit 1; }
[[ -f .env.release && -f .env.routing && -d runtime/classic ]] || exit 1
git fetch origin dev
[[ $(git rev-parse origin/dev) == "$sha" ]] || { echo 'Stale deployment'; exit 1; }
git merge-base --is-ancestor HEAD "$sha" || exit 1
git diff --quiet HEAD "$sha" -- apps/unity-web docs/head/UNITY_ARTIFACT_MANIFEST.json || { echo "Unity changes require a separate deployment"; exit 1; }
stage=$(mktemp -d "$(git rev-parse --git-dir)/classic-gateway.XXXXXX")
trap 'rm -rf "$stage"' EXIT
git archive "$sha" | tar -x -C "$stage"
docker inspect gamecenter-shinomiya-unity-web > "$stage/unity-before.json"
docker inspect gamecenter-shinomiya-classic > "$stage/classic-before.json"
python3 "$stage/scripts/check-classic-gateway.py" --live-classic "$stage/classic-before.json" "$repo"
mkdir -p runtime/deploy
receipt="$repo/runtime/deploy/classic-gateway-${sha}-$(date -u +%Y%m%dT%H%M%SZ).json"
docker inspect gamecenter-shinomiya-classic gamecenter-shinomiya-gateway > "$stage/previous-images.json"
python3 - "$receipt" "$stage/previous-images.json" "$(git rev-parse HEAD)" "$sha" <<'PYRECEIPT'
import json,sys
images=json.load(open(sys.argv[2]))
data={'previousCheckout':sys.argv[3],'requestedSha':sys.argv[4],'phase':'preflight','status':'running','previousImages':[{k:v[k] for k in ['Name','Id','Image']}|{'tag':v['Config']['Image']} for v in images]}
with open(sys.argv[1],'w') as f: json.dump(data,f,indent=2)
PYRECEIPT
phase=preflight
record_exit() {
 code=$?; trap - EXIT
 python3 - "$receipt" "$phase" "$code" <<'PYRECEIPT'
import json,sys
p=sys.argv[1];data=json.load(open(p));data.update(phase=sys.argv[2],exitCode=int(sys.argv[3]),status='local-verified-public-pending' if sys.argv[3]=='0' else 'failed')
with open(p,'w') as f:json.dump(data,f,indent=2)
PYRECEIPT
 rm -rf "$stage"; exit "$code"
}
trap record_exit EXIT
# Only the two target tags change. RELEASE_TAG continues to identify existing Unity.
export CLASSIC_RELEASE_TAG="$sha" GATEWAY_RELEASE_TAG="$sha"
docker compose --project-directory "$repo" --env-file "$repo/.env.release" --env-file "$repo/.env.routing" -f "$stage/compose.dev.yaml" -f "$stage/compose.public.yaml" config --format json > "$stage/config.json"
python3 "$stage/scripts/check-classic-gateway.py" "$stage/config.json" "$stage/unity-before.json" "$repo" "$sha"
# Build immutable images before changing checkout or any running service.
phase=build
docker build -f "$stage/apps/classic/Dockerfile" -t "gamecenter-shinomiya-classic:$sha" "$stage"
docker build -f "$stage/gateway/Dockerfile" -t "gamecenter-shinomiya-gateway:$sha" "$stage"
python3 "$stage/scripts/check-classic-gateway.py" --runtime "$repo/runtime/classic"
docker inspect gamecenter-shinomiya-classic gamecenter-shinomiya-gateway --format '{{.Name}} {{.Config.Image}} {{.Image}}'
previous=$(git rev-parse HEAD); echo "Previous checkout: $previous; new release: $sha"
phase=checkout
git merge --ff-only "$sha"
compose=(docker compose --env-file .env.release --env-file .env.routing -f compose.dev.yaml -f compose.public.yaml)
phase=classic-update
"${compose[@]}" up -d --no-build --no-deps --force-recreate classic
# Recreate nginx after classic so its upstream DNS is resolved again.
phase=gateway-update
"${compose[@]}" up -d --no-build --no-deps --force-recreate gateway
phase=local-verification
"${compose[@]}" exec -T gateway nginx -t
curl --fail --retry 6 --retry-connrefused --retry-delay 3 --max-time 10 http://127.0.0.1:18094/01/api/status
curl --fail --retry 3 --max-time 10 http://127.0.0.1:18094/02/healthz
docker inspect gamecenter-shinomiya-classic gamecenter-shinomiya-gateway > "$stage/current-images.json"
python3 - "$stage/current-images.json" "$sha" <<'PY'
import json,sys
images=json.load(open(sys.argv[1])); sha=sys.argv[2]
for name,item in zip(['classic','gateway'],images):
 assert item['State']['Running'] and item['Config']['Image']=='gamecenter-shinomiya-'+name+':'+sha
assert 'GIT_HASH='+sha in images[0]['Config']['Env']
PY
docker inspect gamecenter-shinomiya-unity-web > "$stage/unity-after.json"
python3 - "$stage/unity-before.json" "$stage/unity-after.json" <<'PY'
import json,sys
before,after=[json.load(open(p))[0] for p in sys.argv[1:]]
for k in ['Id','Image','RestartCount']: assert before[k]==after[k], k
assert before['State']['StartedAt']==after['State']['StartedAt'] and after['State']['Running']
PY
# Preserve original RELEASE_TAG and routing; persist just the two component tags.
phase=persist-component-tags
python3 - "$sha" <<'PY'
import pathlib,sys,os
p=pathlib.Path('.env.release'); original=p.read_text(); lines=original.splitlines()
lines=[x for x in lines if not x.startswith(('CLASSIC_RELEASE_TAG=','GATEWAY_RELEASE_TAG='))]
new='\n'.join(lines)+f'\nCLASSIC_RELEASE_TAG={sys.argv[1]}\nGATEWAY_RELEASE_TAG={sys.argv[1]}\n'
tmp=p.with_name('.env.release.next'); tmp.write_text(new); os.chmod(tmp,p.stat().st_mode & 0o777); os.replace(tmp,p)
PY
phase=local-complete-public-check-pending
echo "Classic/gateway release $sha; Unity container and image unchanged. Runtime was not copied or restored."
# Failure stops, never reset --hard, compose down, prune or automatic data rollback.
REMOTE
