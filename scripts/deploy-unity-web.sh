#!/usr/bin/env bash
# Run on BASE via an ayano-panel generated stdin script. No credentials are inputs.
# deploy publishes provisionally; finalize needs an actual public-browser report.
set -Eeuo pipefail
root=/home/shino/source/repos/upstream/gamecenter-shinomiya
public=https://unity-games.wos.ktsys.jp/02/
mode=${1:-}; argument=${2:-}; browser_report=${3:-}
[[ $mode == deploy || $mode == finalize || $mode == rollback || $mode == retry ]] || { echo 'Usage: deploy-unity-web.sh deploy SHA | finalize RECEIPT_DIR BROWSER_JSON | rollback RECEIPT_DIR | retry RECEIPT_DIR'; exit 2; }
cd "$root"
[[ $(git rev-parse --show-toplevel) == "$root" && $(git branch --show-current) == dev ]] || exit 1
[[ -z $(git status --porcelain --untracked-files=normal) ]] || { echo 'Dirty live checkout'; exit 1; }
case $(git remote get-url origin) in
  https://github.com/ssnshino/gamecenter-shinomiya|https://github.com/ssnshino/gamecenter-shinomiya.git|git@github.com:ssnshino/gamecenter-shinomiya.git) ;;
  *) echo 'Unexpected origin'; exit 1;;
esac
[[ -f .env.release && -f .env.routing ]] || exit 1
exec 9>"$(git rev-parse --git-dir)/classic-gateway-deploy.lock"
flock -n 9 || { echo 'Another gamecenter release is active'; exit 1; }
[[ $(df -PB1 "$root" | awk 'NR==2 {print $4}') -ge 2147483648 ]] || { echo 'Less than 2 GiB free; no build was started'; exit 1; }
compose=(docker compose --project-directory "$root" --env-file "$root/.env.release" --env-file "$root/.env.routing" -f "$root/compose.dev.yaml" -f "$root/compose.public.yaml")
stage=''; receipt=''; guard=''; changed=false; phase=preflight

record() { python3 "$guard" receipt "$receipt/receipt.json" "$1" "${2:-0}"; }
wait_health() {
  local attempt
  for attempt in 1 2 3 4 5 6; do
    if docker exec gamecenter-shinomiya-unity-web node -e 'fetch("http://127.0.0.1:3000/healthz").then(r=>r.json()).then(v=>process.exit(v.ok===true&&v.service==="gamecenter-shinomiya-unity-web"?0:1)).catch(()=>process.exit(1))' </dev/null; then return 0; fi
    sleep 2
  done
  return 1
}
reload_gateway() {
  "${compose[@]}" exec -T gateway nginx -t </dev/null
  "${compose[@]}" exec -T gateway nginx -s reload </dev/null
}
roll_back() {
  local old_sha
  old_sha=$(python3 - "$receipt/before.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['releaseValues']['RELEASE_TAG'])
PY
)
  [[ $old_sha =~ ^[a-f0-9]{40}$ ]] || return 1
  python3 "$guard" capture "$root" "$receipt/recovery-start.json" --allow-unhealthy-unity || return 1
  python3 "$guard" scope "$root" "$(git rev-parse HEAD)" "$sha" || return 1
  python3 "$guard" recovery-preflight "$receipt/before.json" "$receipt/recovery-start.json" "$receipt/proposed-manifest.json" "$sha" "$receipt/built-image-id.txt" "$receipt/.env.release.before" || return 1
  [[ $(docker image inspect "gamecenter-shinomiya-unity-web:$old_sha" --format '{{.Id}}') == $(cat "$receipt/rollback-image-id.txt") ]] || return 1
  python3 "$guard" restore-release "$root" "$receipt/before.json" "$receipt/recovery-start.json" "$sha" "$receipt/.env.release.before" || return 1
  export RELEASE_TAG="$old_sha"
  "${compose[@]}" up -d --no-build --no-deps --force-recreate unity-web </dev/null || return 1
  wait_health || return 1
  reload_gateway || return 1
  node "$receipt/smoke-game-delivery.mjs" "$receipt/previous-manifest.json" http://127.0.0.1:18094/02/ "$root" || return 1
  node "$receipt/smoke-game-delivery.mjs" "$receipt/previous-manifest.json" "$public" "$root" || return 1
  python3 "$guard" capture "$root" "$receipt/rolled-back.json" || return 1
  python3 "$guard" same-checkout "$receipt/recovery-start.json" "$receipt/rolled-back.json" || return 1
  python3 "$guard" verify "$receipt/before.json" "$receipt/rolled-back.json" "$receipt/proposed-manifest.json" "$sha" rollback || return 1
  python3 "$guard" recovered-receipt "$receipt/before.json" "$receipt/rolled-back.json" "$receipt/receipt.json"
}
on_error() {
  local code=$?
  trap - ERR
  set +e
  if [[ -n $receipt && -n $guard ]]; then
    record "failed-$phase" "$code"
    if [[ $changed == true ]]; then
      if ! roll_back; then record rollback-failed "$code"; echo 'Rollback failed. Preserve receipt and inspect actual state before another operation.' >&2; fi
    fi
  fi
  [[ -z $stage ]] || rm -rf "$stage"
  exit "$code"
}
trap on_error ERR

if [[ $mode == deploy ]]; then
  sha=$argument
  [[ $sha =~ ^[a-f0-9]{40}$ ]] || exit 2
  previous=$(git rev-parse HEAD)
  git fetch origin dev </dev/null
  [[ $(git rev-parse origin/dev) == "$sha" ]] || { echo 'Requested release is not current origin/dev'; exit 1; }
  stage=$(mktemp -d "$(git rev-parse --git-dir)/unity-colony.XXXXXX")
  git archive "$sha" | tar -x -C "$stage"
  guard="$stage/scripts/check-unity-web-release.py"
  python3 "$guard" scope "$root" "$previous" "$sha"
  receipt="$root/runtime/deploy/unity-colony-$sha-$(date -u +%Y%m%dT%H%M%SZ)"
  mkdir -m 700 -p "$receipt"
  cp "$guard" "$receipt/check-unity-web-release.py"
  cp "$stage/scripts/deploy-unity-web.sh" "$receipt/deploy-unity-web.sh"
  cp "$stage/scripts/smoke-game-delivery.mjs" "$stage/scripts/verify-game-delivery.mjs" "$receipt/"
  cp "$stage/docs/head/UNITY_ARTIFACT_MANIFEST.json" "$receipt/proposed-manifest.json"
  # Metadata helpers only; no user data, environment body or credentials are copied.
  python3 "$guard" capture "$root" "$receipt/before.json"
  python3 "$guard" backup-release "$root" "$receipt/before.json" "$receipt/.env.release.before"
  python3 - "$receipt" "$sha" "$public" <<'PY'
import importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
root=pathlib.Path(sys.argv[1]);before=json.loads((root/'before.json').read_text())
spec=importlib.util.spec_from_file_location('release_guard',root/'check-unity-web-release.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
helper.write_json(root/'previous-manifest.json',before['artifactManifest'])
helper.write_json(root/'release-tags.before.json',before['releaseValues'])
helper.write_json(root/'receipt.json',{'schema':1,'requestedSha':sys.argv[2],'previousCheckout':before['checkoutSha'],'publicBase':sys.argv[3],'phase':'preflight','adoptionComplete':False})
PY
  python3 "$guard" preflight "$receipt/before.json" "$receipt/proposed-manifest.json"
  # Prove the source's complete inventory, retaining declared per-game metadata.
  SOURCE_SHA=$(python3 - "$receipt/proposed-manifest.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['sourceSha'])
PY
) node "$stage/scripts/verify-game-delivery.mjs" "$stage" "$receipt/regenerated-manifest.json"
  cmp "$receipt/regenerated-manifest.json" "$receipt/proposed-manifest.json"
  docker image inspect "gamecenter-shinomiya-unity-web:$(python3 - "$receipt/before.json" <<'PY'
import json,sys
print(json.load(open(sys.argv[1]))['releaseValues']['RELEASE_TAG'])
PY
)" --format '{{.Id}}' > "$receipt/rollback-image-id.txt"
  python3 "$guard" image "$receipt/before.json" "$receipt/rollback-image-id.txt"
  phase=build; record "$phase"
  docker build -f "$stage/apps/unity-web/Dockerfile" -t "gamecenter-shinomiya-unity-web:$sha" "$stage" </dev/null
  docker image inspect "gamecenter-shinomiya-unity-web:$sha" --format '{{.Id}}' > "$receipt/built-image-id.txt"
  # Recheck before any switch; build must not alter an existing service or data.
  python3 "$guard" capture "$root" "$receipt/pre-switch.json"
  python3 "$guard" same-unity "$receipt/before.json" "$receipt/pre-switch.json"
  python3 "$guard" verify "$receipt/before.json" "$receipt/pre-switch.json" "$receipt/proposed-manifest.json" "$sha" rollback
  export RELEASE_TAG="$sha"
  python3 "$guard" compose "$root" "$receipt/before.json" "$sha"
  phase=unity-update; record "$phase"; changed=true
  "${compose[@]}" up -d --no-build --no-deps --force-recreate unity-web </dev/null
  phase=health; record "$phase"; wait_health
  reload_gateway
  phase=artifact-verification; record "$phase"
  node "$stage/scripts/smoke-game-delivery.mjs" "$receipt/proposed-manifest.json" http://127.0.0.1:18094/02/ "$stage"
  node "$stage/scripts/smoke-game-delivery.mjs" "$receipt/proposed-manifest.json" "$public" "$stage"
  python3 "$guard" capture "$root" "$receipt/provisional.json"
  python3 "$guard" image "$receipt/provisional.json" "$receipt/built-image-id.txt"
  python3 "$guard" verify "$receipt/before.json" "$receipt/provisional.json" "$receipt/proposed-manifest.json" "$sha" provisional
  record awaiting-browser
  rm -rf "$stage"; stage=''; changed=false
  echo "Provisional public Unity release $sha. Browser acceptance and RELEASE_TAG persistence are pending. Receipt: $receipt"
  exit 0
fi

receipt=$(realpath "$argument")
[[ $receipt == "$root"/runtime/deploy/unity-colony-* && $receipt != *'/../'* ]] || exit 2
guard="$receipt/check-unity-web-release.py"
python3 "$guard" receipt-action "$receipt/receipt.json" "$mode"
sha=$(python3 - "$receipt/receipt.json" <<'PY'
import json,sys
v=json.load(open(sys.argv[1]));print(v['requestedSha'])
PY
)
[[ $sha =~ ^[a-f0-9]{40}$ ]] || exit 2
if [[ $mode == rollback ]]; then
  phase=manual-rollback; record "$phase"
  roll_back
  exit 0
fi

if [[ $mode == retry ]]; then
  phase=retry-preflight
  python3 "$guard" capture "$root" "$receipt/retry-current.json"
  python3 "$guard" scope "$root" "$(git rev-parse HEAD)" "$sha"
  git fetch origin dev </dev/null
  [[ $(git rev-parse origin/dev) == "$sha" ]] || { echo 'Retry target is no longer current origin/dev'; exit 1; }
  python3 "$guard" prepare-retry "$receipt/before.json" "$receipt/retry-current.json" "$receipt/proposed-manifest.json" "$sha" "$receipt/built-image-id.txt" "$receipt/.env.release.before" "$receipt/attempt-before.json"
  [[ $(docker image inspect "gamecenter-shinomiya-unity-web:$sha" --format '{{.Id}}') == $(cat "$receipt/built-image-id.txt") ]] || { echo 'Recorded built image is no longer available'; exit 1; }
  export RELEASE_TAG="$sha"
  python3 "$guard" compose "$root" "$receipt/attempt-before.json" "$sha"
  phase=unity-update; record "$phase"; changed=true
  "${compose[@]}" up -d --no-build --no-deps --force-recreate unity-web </dev/null
  phase=health; record "$phase"; wait_health; reload_gateway
  phase=artifact-verification; record "$phase"
  # The checkout may be old after a pre-merge failure. Catalogs are protected
  # and byte-identical, so they are a valid API comparison source in either case.
  node "$receipt/smoke-game-delivery.mjs" "$receipt/proposed-manifest.json" http://127.0.0.1:18094/02/ "$root"
  node "$receipt/smoke-game-delivery.mjs" "$receipt/proposed-manifest.json" "$public" "$root"
  python3 "$guard" capture "$root" "$receipt/provisional.json"
  python3 "$guard" image "$receipt/provisional.json" "$receipt/built-image-id.txt"
  python3 "$guard" verify "$receipt/attempt-before.json" "$receipt/provisional.json" "$receipt/proposed-manifest.json" "$sha" provisional
  record awaiting-browser; changed=false
  echo "Retried the recorded Unity image. New public-browser acceptance is required. Receipt: $receipt"
  exit 0
fi

attempt_before="$receipt/before.json"
if [[ -f $receipt/attempt-before.json ]]; then attempt_before="$receipt/attempt-before.json"; fi
[[ -f $browser_report ]] || { echo 'A completed public-browser report is required'; exit 2; }
python3 "$guard" browser "$browser_report" "$sha" "$receipt/proposed-manifest.json"
python3 "$guard" scope "$root" "$(git rev-parse HEAD)" "$sha"
phase=final-health; changed=true
wait_health
reload_gateway
python3 "$guard" capture "$root" "$receipt/final-preflight.json"
python3 "$guard" image "$receipt/final-preflight.json" "$receipt/built-image-id.txt"
python3 "$guard" same-unity "$receipt/provisional.json" "$receipt/final-preflight.json"
python3 "$guard" verify "$attempt_before" "$receipt/final-preflight.json" "$receipt/proposed-manifest.json" "$sha" provisional
# Keep recovery armed across both final writes. A known requested checkout is
# retained on recovery; the receipt explicitly requires a bounded retry.
phase=finalize-checkout; record "$phase"
git merge --ff-only "$sha" </dev/null
phase=persist-release-tag; record "$phase"
python3 "$guard" persist "$root" "$receipt/before.json" "$sha"
phase=copy-browser-report; record "$phase"
if [[ $(realpath "$browser_report") != "$receipt/browser-acceptance.json" ]]; then cp "$browser_report" "$receipt/browser-acceptance.json"; fi
phase=final-capture; record "$phase"
python3 "$guard" capture "$root" "$receipt/finalized.json"
python3 "$guard" image "$receipt/finalized.json" "$receipt/built-image-id.txt"
phase=final-verification; record "$phase"
python3 "$guard" verify "$attempt_before" "$receipt/finalized.json" "$receipt/proposed-manifest.json" "$sha" finalized
record accepted; changed=false
echo "Accepted public Unity release $sha. Only Unity RELEASE_TAG was persisted. Receipt: $receipt"
