<!-- MOBILE_QUALITY_FIXED_START -->
## 現在: スマホは軽量固定、配備採用完了（2026-10-16）

配布release/永続RELEASE_TAG c6ad33dbb2507cd22c36c207b70f6679bbb368d3、engine source937b98a、Web template sourceba32cf8。Actions38860158039 success、公開10checks/6operations PASS、accepted/adoptionComplete true。iPhoneで軽量は走行でき、詳細切替で落ちるとユーザー確認したためtouchを軽量固定にした。PC切替は維持。今回の実iPhone再読込は未確認。市街地の影は未解消、地区間道路は良好というユーザー観察。

別作業の停止済みALADDIN検証container3個の削除をユーザーが確認し、元の失敗記録を保持した別reviewed receiptで復旧。通常保護コードは不変、他サービス/データ/configを再検証。1エリアCore重視は提案段階で未実装。詳細と復元はdocs/head/MOBILE_QUALITY_GUARD_20261016.md。以前の入口はdocs/history/20261016-before-quality-guard-adoptionへexact bytes/hashで保全。以下は各時点の履歴。
<!-- MOBILE_QUALITY_FIXED_END -->

<!-- MOBILE_LIGHTING_ACCEPTED_START -->
## 現在: スマホ照明修正版を公開（2026-10-16）

照明修正版を公開採用。Unity source `937b98ac785d59354c61c1a3299caaac867a8455`、配布release/Unity RELEASE_TAG `40db65b345aea1ee025b8d83b5d858e4c216c4a9`。Actions run38853563393 success、公開10checks/6operations PASS、receipt accepted/adoptionComplete true/exitCode0、retryRequired/mixedCheckout false。実iPhoneの再確認は待ち。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=lighting-20261016 。軽量でも対応デバイスはHDR/Neutralトーンマップを保持、AOはOFF。Web主光0.85、影強度0.60、露出0、ミラー受光0.15。影距離45/100mとLOD・物理は維持。高速道路/環状線/IC/JCT・N/S長距離道路・山/追加地形・森林は引き続きオミット、コード/元データ保持。

元Scene/Prefab hash不変、Infrastructure767mesh/482collider/3,325,408 summed verticesは起動成功版と同一。data57,353,448bytes/展開後100,944,814bytes。AirRace・旧StreamingAssets/TemplateDataはmanifest照合で保持。ローカルEdge27/WebKit26 PASS。同一視点の遠方路面190x40pixelの白画素率81.26%→0%。PCスクリーンショット比較であり実iPhoneの性能・見え方の証明ではない。

復元先: 市街地切り分け版8c0b9e52590ad0ff00c534f55522012bc278579e（実iPhone17起動・走行済み）、full版f75d8649bb6112326355c45b26f91bd66265f228。Windows EditorのPlay初期化は別件として未検証、Webの走行PASSに読み替えない。

詳細: docs/head/MOBILE_LIGHTING_WEB_20261016.md。以前の記載は各時点の履歴。
<!-- MOBILE_LIGHTING_ACCEPTED_END -->

<!-- CITY_DIAGNOSTIC_ACCEPTED_START -->
## 現在: 市街地切り分け版がiPhone 17で起動・走行（2026-10-16）

Unity source d30013583556733cadb80d1cb043af65272c7d5e、配布release/Unity RELEASE_TAG8c0b9e52590ad0ff00c534f55522012bc278579e。Actions38846295459 success、公開9checks/6operationsとreceipt accepted/adoptionComplete true/exitCode0を確認。iPhone 17で開始画面・走行の実機確認あり。写真HUD118〜120km/h・接地、軽量26〜30fps/詳細34fpsはその時点の表示で持続性能保証ではない。

高速道路・環状線/IC/JCT・長距離地上道・山/追加景観地形をcity-diagnosticで一時オミット。市街地3地区・元の橋・鉄骨・安全内壁/採光帯・街区LODは保持。data57,351,365bytes/展開後100,916,295bytes。ローカルEdge22/WebKit21 PASS。通常/診断/再読込/通常復帰の生成検証もPASS。元データは保存されfullへ切替可能。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=city-diagnostic-20261016 。前便forest版も実機では起動前クラッシュした。今回写真では遠方白飛び・近景の平坦さが残り、軽量/詳細切替でも改善しない。照明調整は次便であり、今回の受入れに含めない。Windows Editor再生成/Play確認もWebの成功と区別する。

詳細: docs/head/CITY_DIAGNOSTIC_WEB_20261016.md。更新前入口資料はdocs/history/20261016-before-city-diagnostic-acceptanceにexact bytes/hashで保全。以下は過去状態の記録。
<!-- CITY_DIAGNOSTIC_ACCEPTED_END -->

<!-- FOREST_WEB_PUBLICATION_START -->
## 現在: 森林なし・遠景街区LODのWebGLを公開採用（2026-10-16）

Unity source `a02c3ae8909e02084a2d44ee7fb2ab6aa19cebc8`（runtimeはd1502bcと同一、Editor native-gzip profile追加）、配布release/Unity RELEASE_TAG `f75d8649bb6112326355c45b26f91bd66265f228`。Actions run 38836767257がsuccess、公開ブラウザ12checks/6operations合格、receipt accepted/adoptionComplete true/exitCode0を確認した。ローカルEdge25・WebKit24と、通常解像度の公開WebKit24もPASS。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=forest-20261016 。森林を生成せず山/道路/JCT/街路樹は保持し、遠い建物は街区モデルへ切替。dataは配信84,612,569bytes／HTTP展開後162,904,246bytes（前便92,787,516／218,766,927）。ブラウザnative gzip、JS展開fallbackなし。実iPhone 17起動はユーザー検証待ち。以下のBrotli対策・ローカル未公開などは各時点の履歴で、今回をiPhone成功と扱わない。

今回の結果は森林なしWeb公開記録を参照。CIの256px software WebGL確認は性能保証ではない。既存classic/gateway・永続data・AirRaceと保持catalog/Bundleをguardで保護し、Unityだけを配備した。
<!-- FOREST_WEB_PUBLICATION_END -->

<!-- IOS_SAFARI_BOOT_START -->
## 現在: iPhone Safariの起動クラッシュに対応（2026-10-15）

ユーザー実機でSafariが繰り返しクラッシュした。PC/WebKit smoke合格をiPhone適合と扱わない。対策版公開済み・iPhone実機の解消は未確認。約93MB→219MBのJS Brotli展開を、ブラウザnative展開へ変更。圧縮byte・展開後byteとUnityゲーム内容は同一。JS/WASMの.br MIMEを補正し、通常Edge/WebKitの確認を行った。実機はiPhone 17、開始ボタンが表示される前にクラッシュすると本人確認済み。原因はメモリ不足の可能性があり、断定していない。

詳細と公開receiptは `docs/head/IOS_SAFARI_BOOT_20261015.md`。以前の公開受入れはPC/ソフトウェアブラウザでの受入れであり、iPhone起動成功の証拠ではない。
<!-- IOS_SAFARI_BOOT_END -->

## 公開採用済み: 2026-10-15 道路網・山地のスマホ用WebGL

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`、配布release／Unity RELEASE_TAG `e36ccaf102ee8494aa0d60d4d347f268114a9924`、Unity image `sha256:36e023b1586b3f7db8d0bce9bbecf629821eb78ee62b3341e21f2f69cc69dada`。Actions run [38742023882](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38742023882) がsuccess、2026-10-15 22:27 JSTにreceipt accepted／adoptionComplete true／exitCode0を確認。公開URLの通常解像度Edge25・WebKit24 checksも合格。実iPhone/Android性能は未測定。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/ 。高架・南/中央/北環状の移動ボタンを追加。既存Actions認証を使うUnity専用自動配備を追加し、公開ブラウザ後にfinalize、失敗時rollbackまで実動作を確認した。classic/gatewayとruntime dataをguardで保持。詳細は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。以下の公開待ち・未実施は各記録時点の履歴。

## 2026-10-15 Unity自動配備の追加（検証・公開待ち）

今回のスマホ向けデプロイ依頼と自動配備の確認を受け、Unity専用 `.github/workflows/deploy-unity-web.yml` を追加。dev更新で既存Actions認証を利用し、Unity限定仮配備、実公開ブラウザでの起動・運転確認、finalizeの順に進め、受入れ失敗時はrollbackする。classic/gateway workflow、鍵、runner、firewallは変更しない。以下の旧作業範囲は記録当時のもの。現在の証拠は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md` に記録し、accepted receipt確認まで公開完了と扱わない。

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
