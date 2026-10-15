# Colony RacerのみのWebGL公開手順

2026-10-14に追加した手順。実装・ローカル試験の記録であり、この文書やscriptの存在を公開済みの証拠としない。公開先は従来と同じ `https://unity-games.wos.ktsys.jp/02/colony-racer/`。実行担当はその時点のRootで、Unityビルド、GitHub反映、BASEの暫定切替、実ブラウザ確認、最終採用を別々に記録する。

## 対象と保持するもの

Unity編集元は既存colony-racer repo。配布正本はgamecenter-shinomiya/dev。新WebGLの `index.html`、`Build/`、`TemplateData/` と入力UIを更新する。AirRace全57ファイルと、Colonyの既存StreamingAssets/catalog/Bundleをbyte単位で保持する。既存Node配信コード、Rust、Compose、gateway設定、workflow、鍵、routing、runtime6JSON、他アプリは変更しない。

このUnity更新では新しい市街地と車体をsceneに含める。旧catalog/Bundleを実行時に再読込して最新sceneの証拠にする構成は採用しない。PCとmobileは同じ公開URLを使用する。入力UIは今回の承認に沿って改善できるが、旧UIファイルを無断削除しない。最新Nativeの120km/h試験はWebGLでの実走検証とは区別する。

## ソース・成果物の固定

1. Unityの新controller、templateとbuilderを検証し、Unity編集元をcommitする。生成WebGLをGitHub上の既存公開へ先に書き込まない。
2. 使用したUnity commit、830等の実際のsource inventory、package/settings inventory、ビルド設定、Unity version、生成物hashを別のbuild記録に残す。件数は今回の実計測値であり固定期待値ではない。
3. 配布repoの最新devからfeatureでColony成果物を更新し、AirRace/既存Colony StreamingAssetsのhashを比較する。圧縮は `.gz` ならContent-EncodingとWASM/JS MIME、`.unityweb` ならUnity fallback loaderの実動作を確認する。
4. manifest生成は旧import由来SHAと今回のUnity source SHAを分離する。

validatorは旧 `buildUrl="Build"` に相対filenameを足す形式、または4つのliteral `Build/<filename>` のみを扱う。literal templateはlocal `preview.css` と `preview.js` の参照・実ファイルも必須。absolute URL、traversal、query付きbuild参照は拒否し、JavaScriptを実行して参照を推測しない。

```bash
SOURCE_SHA=<manifestに残す配布取り込み元の40桁SHA> \
COLONY_UNITY_SOURCE_SHA=<今回実際にビルドしたUnityの40桁commit> \
COLONY_UNITY_BUILD_PERFORMED=true \
node scripts/verify-game-delivery.mjs . docs/head/UNITY_ARTIFACT_MANIFEST.json
node --test tests/game-delivery.test.mjs
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_unity_web_release.py -v
bash -n scripts/deploy-unity-web.sh
```

schema1のColony game entryに `unitySourceSha` と `unityBuildPerformed:true` を付ける。AirRaceの未確認Unity source SHAを推測して埋めない。top-level `sourceSha` は取り込み元履歴、`unitySourceSha:null` は2ゲーム一括のUnity SHAを断定しないこと、`unityBuildPerformed` は少なくとも1ゲームをビルドしたことを表す。既存CIの通常再生成は、同じsourceShaの保管manifestから宣言済みColony由来metadataだけを引き継ぎ、全ファイルhashを実物から計算する。metadata引継ぎ自体はUnity build provenanceの検証ではない。

featureのCIと差分確認後、通常のPR→devへ反映する。既存classic/gateway workflowはUnity更新に使わない。Unity差分とmanifestはその経路で配備しないというguardを保持する。配布SHAはdev merge後の実際の40桁SHAに固定する。

## BASEの読取確認

workspaceのayano guidance/capabilityと各repo入口を読み、`ayano-panel ssh remote-bundle` でSSH stdin形式を生成する。手書きの入れ子quoteでremote操作を組み立てない。

```text
ayano-panel ssh remote-bundle --host base --workdir /home/shino/source/repos/upstream/gamecenter-shinomiya --interpreter bash --json
```

接続は既存信頼済みhost keyを厳格検証する。再確認項目は実checkout/dev/SHA/clean、origin、Compose labelsと実mount、稼働3imageとStartedAt/restarts、実image内114資産のhash、runtime6JSONのhash/所有者、routing・Compose・gateway設定hash、空き容量・負荷。他アプリのinspectは識別・state・image・StartedAt等だけを保存し、Envやユーザーデータ本文を保存しない。

2026-10-14調査時のUnity serviceはimage内 `/app/public/colony-racer`、readonly、mountなし。従ってrsync/docker cpで稼働containerへ上書きする方式ではない。旧image `041e0548362a2040bfd94d518866a04456849e05` は調査時点で現存した。これらは歴史的チェックポイントなので実行直前に再確認する。

## 1. 暫定公開

BASE checkoutはcleanな旧devのまま、origin/devをfetchして指定SHAが最新か確認する。実行script自身も指定SHAのGit objectから取り出す。Rootは以下をayano生成stdinへ渡す。

```bash
sha=<対象devの40桁SHA>
git fetch origin dev </dev/null
test "$(git rev-parse origin/dev)" = "$sha"
script=$(mktemp /tmp/gamecenter-unity-deploy.XXXXXX)
trap 'rm -f "$script"' EXIT
git show "$sha:scripts/deploy-unity-web.sh" > "$script"
bash "$script" deploy "$sha"
```

scriptは既存classic/gateway lockを共有し、以下を順次行う。

- 差分をColony資産、今回の限定helper/tests、資料に限定。AirRace資産、既存Colony StreamingAssets、配信コード、Compose/gateway/workflowの変更は拒否。
- 現在のimage・tags・release設定hashと全対象外container、runtime hashをreceiptへ保存。release設定は既知3タグだけを許容し、秘密値を保存しない。
- 固定配布SHAをGit archiveしてUnity imageだけをbuild。旧image/tagを消さない。build後に保持対象の実状態を再確認する。
- 当該Compose処理のRELEASE_TAGだけ新SHAにし、`up -d --no-build --no-deps --force-recreate unity-web`。classic/gatewayのcontainerを作り直さない。
- Node自身のhealthを待ち、gatewayで `nginx -t </dev/null` と `nginx -s reload </dev/null`。gateway image/containerを保持し、DNSだけを再解決する。
- local/publicで全2ゲーム資産、gzip復号hash、MIME、catalog APIを照合。実image ID、他container、runtime、routingの保持を照合。

成功時は `runtime/deploy/unity-colony-<SHA>-<UTC>/receipt.json` が `awaiting-browser` になる。URLでは新WebGLが暫定公開されているが、Git checkoutと永続RELEASE_TAGは旧値。Rootは続けて実ブラウザ検証とfinalizeを行う。この状態を公開完了と報告しない。

health/hash/preservation検査失敗時は、旧Unity imageだけを再作成、gatewayをgraceful reload、旧114ファイル・APIと保持対象を再照合する。runtimeを復元しない。rollback自体が失敗したら `rollback-failed` を記録して停止し、実状態を調べる。build/新切替の自動再実行、reset --hard、compose down、image GC、他アプリ更新はしない。

## 2. 実ブラウザ検証と採用

Rootは公開URLで読み込み、加速、制動、左右操舵、reset、Core/East/West地区を実操作する。120km/h接地をWebGLでも計測する場合はその実値を記録し、Native結果の転記で済ませない。mobile入力は実機とdesktop touch emulationを区別する。

ブラウザ受入記録の最低構造は以下。値や観察は実際の結果で埋める。session/cookie/tokenを含めない。

```json
{
  "complete": true,
  "pass": true,
  "distributionSha": "実配布40桁SHA",
  "unitySourceSha": "実Unity40桁SHA",
  "url": "https://unity-games.wos.ktsys.jp/02/colony-racer/",
  "observations": [
    { "name": "loaded", "pass": true, "observedUtc": "実日時", "tool": "実ブラウザtool" }
  ]
}
```

observationsに `loaded/accelerate/brake/steer/reset/districts` の6種類が必要。画像・HUD/telemetryなどの追加証拠は別のQA記録へ残す。ファイルを既存SSHのstdinなどでBASEのreceipt内へ安全に転送し、次をayano生成remote scriptで実行する。

```bash
bash <receipt-dir>/deploy-unity-web.sh finalize <receipt-dir> <browser-report-json>
```

finalizeは同じ稼働Unity image/container、保持対象、sourceとブラウザreportを再照合する。成功後だけGit devを固定SHAへfast-forwardし、.env.releaseのRELEASE_TAG1項目をatomicに保存する。classic/gatewayの個別タグとroutingは保持。mergeにも `</dev/null` を付け、hookへSSHの残りのstdin scriptを渡さない。最後のcapture/checkが成功するとreceiptは `accepted`。

merge直前、merge後・tag保存前、tag保存後・最終検証のいずれの失敗でも復旧を有効にしておく。復旧は、clean dev HEADが最初のcheckout SHAかrequested SHAだけ、Unity image/tagが記録済み旧版か実buildした新版だけ、環境ファイルがbackup原文か既知RELEASE_TAG1項目だけを変えた原文だけ、他tags/container/runtime/routingが最初の状態と同一、というguard後に行う。条件外なら `rollback-failed` を残して停止し、盲目的resetやdata復元を行わない。Unityが異常停止してasset inventoryを取れない場合は未観測を明示し、正確な既知Docker image IDで復旧を限定する。復旧後は旧版の実asset inventory・health・公開hash/APIを確認する。

merge前の失敗ならreceiptは `rolled-back`。merge後の失敗ならGitのrequested checkoutを保持し、旧imageと旧RELEASE_TAGを戻して `rolled-back-mixed-checkout-awaiting-retry` にする。後者はcheckoutの新manifestと実公開旧assetsが異なる状態であり、採用完了や完全な旧checkout復帰とは呼ばない。`mixedCheckout:true/adoptionComplete:false/retryRequired:true` と実checkout SHAをreceiptへ保存する。

ブラウザで失敗した暫定版を戻す場合：

```bash
bash <receipt-dir>/deploy-unity-web.sh rollback <receipt-dir>
```

このrollbackは未finalizeと既知finalize失敗phase、`rollback-failed` のreceiptが対象。同じbounded guardで実状態を照合する。`accepted` 後の復帰は別に現在のcheckout/tag/imageとdataを照合して手順をレビューする。

## 失敗後の限定retry

SSH切断等でERR trapが動かなかった時も、`unity-update/finalize-checkout/persist-release-tag/final-verification` 等の既知in-progress phaseから同じguard付きrollbackを実行できる。flockが生きた元processとの競合を防ぐ。receiptとsnapshotはowned unique tempへfsyncしてatomicに置換し、中断でJSONを途中まで上書きしない。tag保存・復元もunique tempを使用し、その操作が作ったtempだけをfinallyでcleanupする。異常終了で残った別tempを上書き・削除せず、次の試行を妨げない。

`rolled-back` または `rolled-back-mixed-checkout-awaiting-retry` からの再公開は、通常deployではなく同じreceiptを使う。

```bash
bash <receipt-dir>/deploy-unity-web.sh retry <receipt-dir>
```

retryは現在のclean known HEAD、旧image/tag/旧実assets、元receiptの保持対象とbackupを照合する。origin/devがまだrequested SHAであり、記録済みbuilt image IDがそのtagに現存することも必要。同じimmutable imageだけを再公開し、新imageを再buildしない。正常な旧版inventoryが取れない時はretryしない。

新attemptの実checkpointを `attempt-before.json` に保存する。実測checkout SHAとそのcheckoutにあるmanifestは変更せず、旧版imageから照合した元receiptのmanifestを `servedArtifactManifest/servedManifestReference` として別fieldで参照する。このため新HEAD＋旧imageの差異を隠さず検証できる。暫定再公開後は `awaiting-browser` に戻り、新しい実ブラウザ検証とfinalizeが必要。通常deployのmanifest不一致を無視するためのfallbackではない。

requested SHA以外の新buildへの更新、他サービスやdataが変化した後の再基準化はこのretryの範囲外。実状態を確認して別の固定SHA・計画へ引き継ぐ。壊れた新版を同じまま何度も再公開しない。

## 完了の証拠

Unity source commit＋build inventory、配布merge SHA、生成asset manifest、実image ID、receipt accepted、公開全hash/API、実ブラウザ観察を対応付ける。HTTP200、Actions success、Native120km/h、scriptの存在のどれか1つでWebGL公開完了とは扱わない。
