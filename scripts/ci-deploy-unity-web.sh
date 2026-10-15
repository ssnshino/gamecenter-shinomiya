#!/usr/bin/env bash
# Uses the existing Actions credentials; no key is installed on a workstation.
set -euo pipefail
mode=${1:-}; receipt=${2:-}; report=${3:-}
[[ $mode == deploy || $mode == finalize || $mode == rollback ]] || exit 2
[[ ${SOURCE_SHA:-} =~ ^[a-f0-9]{40}$ ]] || exit 2
root=/home/shino/source/repos/upstream/gamecenter-shinomiya
[[ ${DEV_DEPLOY_REPO_PATH:-} == "$root" ]] || exit 2
[[ ${DEV_DEPLOY_HOST:-} =~ ^[a-zA-Z0-9][a-zA-Z0-9.-]*$ ]] || exit 2
[[ ${DEV_DEPLOY_PORT:-} =~ ^[0-9]+$ ]] || exit 2
(( DEV_DEPLOY_PORT > 0 && DEV_DEPLOY_PORT < 65536 )) || exit 2
[[ -n ${DEV_DEPLOY_SSH_KEY:-} && -n ${DEV_DEPLOY_KNOWN_HOSTS:-} ]] || exit 2
if [[ $mode != deploy ]]; then
  [[ $receipt =~ ^$root/runtime/deploy/unity-colony-$SOURCE_SHA-[0-9]{8}T[0-9]{6}Z$ ]] || exit 2
fi
payload=''
if [[ $mode == finalize ]]; then
  python3 scripts/check-unity-web-release.py browser "$report" "$SOURCE_SHA" docs/head/UNITY_ARTIFACT_MANIFEST.json
  payload=$(base64 -w0 < "$report")
fi
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
chmod 700 "$work"
printf '%s\n' "$DEV_DEPLOY_SSH_KEY" > "$work/key"
printf '%s\n' "$DEV_DEPLOY_KNOWN_HOSTS" > "$work/known_hosts"
chmod 600 "$work/key" "$work/known_hosts"
unset DEV_DEPLOY_SSH_KEY
mkdir -p runtime-ci
ssh -i "$work/key" -p "$DEV_DEPLOY_PORT" -o BatchMode=yes -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile="$work/known_hosts" -o ConnectTimeout=20 \
  "shino@$DEV_DEPLOY_HOST" "bash -s -- '$root' '$SOURCE_SHA' '$mode' '$receipt' '$payload'" <<'REMOTE' | tee "runtime-ci/$mode.log"
set -euo pipefail
root=$1; sha=$2; mode=$3; receipt=$4; payload=$5
cd "$root"
[[ $(git rev-parse --show-toplevel) == "$root" && $(git branch --show-current) == dev ]] || exit 1
[[ $sha =~ ^[a-f0-9]{40}$ ]] || exit 2
if [[ $mode == deploy ]]; then
  git fetch origin dev </dev/null
  [[ $(git rev-parse origin/dev) == "$sha" ]] || { echo 'Stale Unity release'; exit 1; }
  script=$(mktemp "$(git rev-parse --git-dir)/unity-ci-entry.XXXXXX")
  trap 'rm -f "$script"' EXIT
  git show "$sha:scripts/deploy-unity-web.sh" > "$script"
  bash "$script" deploy "$sha" </dev/null
else
  [[ $receipt =~ ^$root/runtime/deploy/unity-colony-$sha-[0-9]{8}T[0-9]{6}Z$ ]] || exit 2
  if [[ $mode == finalize ]]; then
    python3 - "$receipt/browser-acceptance.json" "$payload" <<'PY'
import base64,json,pathlib,sys
value=json.loads(base64.b64decode(sys.argv[2],validate=True))
pathlib.Path(sys.argv[1]).write_text(json.dumps(value,indent=2)+'\n')
PY
    bash "$receipt/deploy-unity-web.sh" finalize "$receipt" "$receipt/browser-acceptance.json" </dev/null
    cat "$receipt/receipt.json"
  elif [[ $mode == rollback ]]; then
    bash "$receipt/deploy-unity-web.sh" rollback "$receipt" </dev/null
  else exit 2; fi
fi
REMOTE
if [[ $mode == deploy ]]; then
  receipt=$(sed -n 's/.*Receipt: \(\/home\/shino\/source\/repos\/upstream\/gamecenter-shinomiya\/runtime\/deploy\/unity-colony-[a-f0-9]*-[0-9TZ]*\)$/\1/p' runtime-ci/deploy.log | tail -1)
  [[ $receipt =~ ^$root/runtime/deploy/unity-colony-$SOURCE_SHA-[0-9]{8}T[0-9]{6}Z$ ]] || exit 1
  [[ -z ${GITHUB_OUTPUT:-} ]] || printf 'receipt=%s\n' "$receipt" >> "$GITHUB_OUTPUT"
fi
