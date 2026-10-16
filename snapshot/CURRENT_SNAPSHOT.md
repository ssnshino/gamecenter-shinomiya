<!-- MOBILE_DOUBLE_TAP_ACCEPTED_START -->
## 現在: ダブルタップ拡大防止版を公開（2026-10-16）

配布release/Unity RELEASE_TAG `004110fd8efd70e1a5890608b8f0cb92a5a36e88`。Actions38863673644 success、公開実ゲーム10checks/6operations PASS、receipt accepted/adoptionComplete true/exitCode0、retryRequired/mixedCheckout false。Web template source fb9df73eb723ed5661ea973bc83c5f8027bd44fe。Unity engine source937b98aの既存buildを使用し、今回Unity再buildはしていない。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=double-tap-20261016 。ゲーム全体にtouch-action、Safariの近接連続tap補助を追加。2本指入力を連続tap判定から除き、button連続操作を保持。純Nodeイベント9条件PASS、CUA実ゲームの起動・品質切替・連続reset・縦横表示/倍率1・console error0を確認。実iPhoneのnative zoom解消はユーザー再確認待ち。

前版はユーザーが軽量化を体感し30fps表示を報告（持続性能測定ではない）。スマホ軽量固定を維持。市街地の影は未解決、1エリアCore重視は相談段階。詳細はdocs/head/MOBILE_DOUBLE_TAP_20261016.md。更新前文書はdocs/history/20261016-before-double-tap-acceptanceへexact bytes/hashで保存。以下は各時点の履歴。
<!-- MOBILE_DOUBLE_TAP_ACCEPTED_END -->

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

## 公開準備中: 2026-10-15 道路網・山地のスマホ用WebGL

Unity `eeca3f261038b6d6bf271b91157b0a5abf23ac9d` から5 IC・3環状線/JCT・盛土中央分離帯・距離案内・DEM山地/森林を含むWebGLを生成。スマホから高架と3環状線へ移動できるボタンを追加。見た目用InfrastructureのCPU meshコピーを除き、森林のみ圧縮、道路Colliderと原Prefabを保持した。Brotli fallbackを使用。AirRace全資産・旧Colony StreamingAssets/TemplateDataをbyte照合して保持。

既存の自動配備はclassic/gatewayのみだったため、既存Actions認証を使うUnity専用workflowを追加。CI・公開受入れ待ちで、公開切替は未実施。記録: `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。更新前3文書は `docs/history/20261015-before-colony-road-network/`。

# 現在地: 2026-10-11 JST — classic/gateway自動配備・公開検証済み

## 最新成果物: 2026-10-15 Colony Racer既存街並みの外観更新

Unity source `a5c3493a9378480e24a54b99bfe169662fbf028b`から新WebGLを生成。Core/East/Westの外観・道路素材・葉の光を改善し、元の構造・物理とPC／touch操作を保持した。ローカル9描画測定、通常3環境88checks、Native先行7と最終近景1を確認。連続接地は未合格、iPhone実機は未測定。成果物と制限は[今回記録](../docs/head/COLONY_STREETSCAPE_20261015.md)。

公開の採用状態は今回rawのpublic-browser-acceptance.jsonとBASE receipt accepted、live Unity image／RELEASE_TAGを照合する。Git mergeやこの文書だけでは公開完了としない。以下の91ef／2026-10-14の『現在』は旧公開の履歴であり、Unity source・配布commit・image・文書commitを区別して再開する。

## 完了（入力・描画prototype公開）: 2026-10-14 Colony Racer共通WebGL

既存Core／East／West、固定躯体・生活街区とP0-P2車体を、[https://unity-games.wos.ktsys.jp/02/colony-racer/](https://unity-games.wos.ktsys.jp/02/colony-racer/) のPC・タッチ共通版へ更新した。PCはW／Space／A・D、スマホは左のアナログ操舵・右の加速と制動。旧公開版にぷにこんがあったという推測は本人確認で訂正し、新しいtouch controllerを採用した。スマホ専用Sites案は中止・未公開。

2026-10-14 23:51 JSTに公開採用を完了した。配布devと永続Unity RELEASE_TAGは `91efbec9032aaa087236e0965d7e0cb16b9ff583`、Unity sourceは `ab3394504e39b7997eeb1e454f82bfb55088ffef`、Unity imageは `sha256:48d91a6cb4d99dc0ff890ad9c63e817e88e59df43ac7c7e05e357933aae4fea6`。accepted receipt／BASE clean checkout／公開PC24checks・touch33checks計528samples／post-final115file hash・gzip・MIME・catalog APIのexit0を照合した。今回の採用は共通controller／render prototypeの公開で、接地安定の受入れとは分ける。

独立 `public-acceptance-audit.json` の7群PASSで同Unity image、対象外132container、runtime6JSON、routing／Compose／gateway設定、AirRace57file、既存Colony StreamingAssets37／TemplateData14を照合した。classic／gatewayはa45dc158のimage／containerを継続し、gatewayはDNS再解決のgraceful reloadだけを行った。runtime dataをGitへ取り込んでいない。

Webの入力・描画smokeと連続接地を区別する。ローカル3環境の88checks／807samplesはsmoke PASS、100km/h以上の近傍路面でcontactが間欠的に外れるため連続接地gateはfalse。motor・操舵はcontactでgateされるのでHUDだけの問題とは扱わない。iPhone hardware・実機fpsは未測定。Native r9の115条件は履歴で、WebGL合格へ転記しない。

結果は [Colony WebGL更新](../docs/head/COLONY_WEBGL_20261014.md)、手順は [Unity限定公開](../docs/head/COLONY_WEBGL_PUBLICATION.md)。source commit・配布commit・image SHA・実URLを別に照合して再開する。以下は更新前の記録で、旧Unity image041e054と『再ビルド／公開未実施』は各記録時点の履歴。

### 今回の公開・再開対応

- Unity実行release: `91efbec9032aaa087236e0965d7e0cb16b9ff583`／image `sha256:48d91a6cb4d99dc0ff890ad9c63e817e88e59df43ac7c7e05e357933aae4fea6`。receipt accepted、adoptionComplete true。
- classic／gateway実行release: `a45dc158dbe1785d971e597ec16d95fe9e77bd4e`。image／containerを再作成せず、gatewayのDNS再解決だけgraceful reloadした。
- AirRace57file、旧Colony StreamingAssets37／TemplateData14、runtime6JSON、routing、対象外132containerを最終receiptと独立監査で再照合した。
- initial failed公開suite2件と切替前guard停止のreceiptを保全し、逐次rerunの採用結果と区別する。
- BASEはclean dev `91efbec9032aaa087236e0965d7e0cb16b9ff583`、永続RELEASE_TAGも同SHA。CLASSIC_RELEASE_TAG／GATEWAY_RELEASE_TAGはa45dc158を保持。文書だけの後続commitは実image変更を意味しない。
- 次回は高速直進のcontact／solverの揺れを別に調査し、完了済み公開を再配備せずlive HEAD／dirty／receiptと実hashを照合する。iPhone実機性能、追加衝突検証は未確認。

統合公開後、本人の「既存の鍵を使う従来方式で完遂」の指示に従い、自動配備を有効化してdevマージによる1回のclassic/gateway配備と公開検証を完了した。Unity編集ソースは各repoに残し、既存配布物・image/container・データを保持した。

## 現在の公開と配備

- 共通入口: https://unity-games.wos.ktsys.jp/
- 1号店: https://unity-games.wos.ktsys.jp/01/
- 2号店: https://unity-games.wos.ktsys.jp/02/
- 配布repo: ssnshino/gamecenter-shinomiya、default/運用branch dev。
- Mac: /Volumes/SSD250GBUSB/source/repos/upstream/gamecenter-shinomiya。
- BASE: /home/shino/source/repos/upstream/gamecenter-shinomiya。
- classic/gateway実行release SHA: a45dc158dbe1785d971e597ec16d95fe9e77bd4e（PR #3のdevマージ）。
- Unity実行release SHA: 041e0548362a2040bfd94d518866a04456849e05。後続の配備script修正・文書commitをimageの実行SHAと混同しない。
- Compose project gamecenter-shinomiya。container/serviceはgamecenter-shinomiya-classic / classic、gamecenter-shinomiya-unity-web / unity-web、gamecenter-shinomiya-gateway / gateway。
- classicとunity-webは内部3000、gatewayの確認ポートは127.0.0.1:18094 → 80。公開gatewayだけを既存wos-proxy-networkへ接続。既存proxy設定ファイル、鍵/firewall/NAT/runnerは変更していない。
- 初回公開切替は2026-10-11 01:12:08 JSTに完了。その後のclassic/gateway自動更新は13:07 JST。3container running/restarts=0。

## 2026-10-11 — 1回の自動配備と保全確認

- [PR #3](https://github.com/ssnshino/gamecenter-shinomiya/pull/3)を04:04:57 UTCにdevへマージ。PRの[Docker CI 38110287938](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110287938)と[verify 38110288061](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110288061)は事前に成功した。
- dev a45dc158dbe1785d971e597ec16d95fe9e77bd4eの[build/deploy 38110443542](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443542)と[verify 38110443571](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443571)はsuccess。既存dev用SecretでSSH接続し、classic→gatewayだけを--no-depsで更新。手動dispatch・再実行は0回。

| service | 実行image tagのSHA | BASEで照合したimage ID |
|---|---|---|
| classic | a45dc158dbe1785d971e597ec16d95fe9e77bd4e | sha256:3f4a29feae5aedf74b2a2d64506618148ee2636efa9338a6753da4f40611608f |
| gateway | a45dc158dbe1785d971e597ec16d95fe9e77bd4e | sha256:23cd0831ae7295e4841839a96ae39b1b78dcf4de9e72485780b505681482b1a5 |
| unity-web | 041e0548362a2040bfd94d518866a04456849e05 | sha256:5aaf891d0e7c167a87e6bfe633f044c15538d2e1483419306542c8616740afbf |

- 各tagが指すimage IDと稼働containerのImageが一致。classicのGIT_HASHはa45dc158dbe1785d971e597ec16d95fe9e77bd4e。classic StartedAt=04:07:22 UTC、gateway=04:07:25 UTC。Unityはcontainer ID 4bc818141ac1623ef74dacb6f45ae3fcbf6aa7a92cffa2a22a94d74985253dbe、StartedAt=2026-10-10 16:09:03 UTC、image/restarts=0を含め前後一致。
- 同じActions runでUnity全114ファイルのHTTP hash・gzip復号・MIME/catalog APIとportal/classic API/WSを検証。追加確認ではHTTP15経路、classic/portal静的24ファイルhash、query保持redirect6件、互換Bundle2件とroot catalog API6比較、classic WS7経路のJSON状態受信が成功。
- Macの実ブラウザでportal/両店menu、Pongの描画と上入力、AirRace ROUND1の開始・飛行・旋回、Colony ROUND2の開始・歩行・旋回を確認。観察したconsole errorは0。スコア・ゴーストを投稿していない。
- Unity114ファイルとmanifestのhash inventoryは配備前と一致。runtime/classicの6JSONは個別hash・サイズ・JSON構造・uid/gid=1000・mode=0644が一致、合計7,177,421 bytesを保持。Unityを含む対象外131コンテナのID/image/state/StartedAt/restartsも前後一致。routingファイルは無変更。Unity再ビルド、旧workflow/旧container再実行、Godot・runner・firewall変更は行っていない。
- 配備後照合で.env.releaseの個別タグ未保存を発見。SSHのbash -sの残りの標準入力をcompose execが読み取ったため、runのBASE stepがnginx -t後に終了していた。公開検証stepは成功。04:12 UTCにlock/clean/稼働SHA/保全guardを再確認し、nginx -t・local health2経路・タグ記録だけを補完した。再build・再作成は行っていない。RELEASE_TAGは旧Unity SHAのまま、CLASSIC_RELEASE_TAG/GATEWAY_RELEASE_TAGはa45dc158dbe1785d971e597ec16d95fe9e77bd4eに保存済み。
- [PR #4](https://github.com/ssnshino/gamecenter-shinomiya/pull/4)の修正はnginx -tへのstdinを/dev/nullにする1行と回帰テスト。修正前の早期終了を再現し、修正後はhealth・保全検証・タグ保存まで到達。ブランチ[Docker CI 38110872759](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110872759)と[verify 38110872746](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110872746)、PRの[Docker CI 38110956338](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110956338)と[verify 38110956411](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110956411)はsuccess。04:18:05 UTCにdevへマージした修正SHAはce2a22b9f25e60f9cd7e250f7afa35ba693d803d。
- PR #4のマージ時だけ配備変数をfalseにし、同SHAの[Docker CI 38111146311](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146311)と[verify 38111146286](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146286)のsuccess・deploy skippedを確認してtrueへ戻した。CIでbuildした修正SHAと、稼働classic/gatewayのa45dc158dbe1785d971e597ec16d95fe9e77bd4eは区別する。アプリ・gateway・Compose・Unityのソース差分はなく、2回目のBASE配備は行っていない。
- 自動配備receiptはruntime/deploy/classic-gateway-a45dc158dbe1785d971e597ec16d95fe9e77bd4e-20261011T040657Z.json。元のphase=local-verification/status=local-verified-public-pending/exitCode=0を保全し、それだけでタグ保存・公開完了と扱わない。公開結果は上記Actions run、補完・前後比較はMacの/tmp/gamecenter-shinomiya-classic-gateway-20261011/に記録。秘密値・data本文は含めていない。

## classic/gateway有効化前の確認（2026-10-11 03:40 UTC / 12:40 JST）

- PR #2は2026-10-11 02:33 UTCにdevへマージ済み。当時のdev SHAは25c625e3ba441655c33cf3e868cfca086cbd2088。
- 同SHAの[Docker build CI run 38105519621](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519621)と[配布検証run 38105519655](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519655)はsuccess。classic/gatewayの実ビルド、nginx設定、Node/Rust検証、成果物manifest照合、guardテストを実施済み。deploy jobはliteral falseによってskipped。
- BASEのcheckoutはclean dev、HEAD d39f535d4248625f9e937247a100e51f1e0944ce。稼働classic/gateway/unity-webのimage tagとclassic GIT_HASHは全て041e0548362a2040bfd94d518866a04456849e05。3container running、restarts=0。CIでビルド済みのSHAを稼働済みとは扱わない。
- この確認時点では新repoのActions SecretsとVariablesは両方空で、設定登録・有効化PRの投稿・devマージは承認待ちだった。後述の本人の継続指示により従来方式で登録した。共通DEPLOY_SSH_KEYや新規鍵を使用しない。
- DEV_DEPLOY_KNOWN_HOSTSのed25519 fingerprintはSHA256:jxrQwD92EJgL/MQZ41cEGG54w+RsgW3FuBHelFoP0Cc。引き継ぎ公開鍵、Macの既存known_hosts、StrictHostKeyChecking=yesの既存BASE接続で得たホスト公開鍵、wos.ktsys.jp:4523の現在の取得値が一致。
- 配備前基準: Unity container/image/StartedAt/restarts、既存114ファイルのhash inventory、runtime/classicの6JSONのhash/サイズ/JSON妥当性/uid=1000を確認。6JSONは合計7,177,421 bytes。data本文や秘密値は記録に含めていない。
- 有効化用の変更はworkflowのliteral false解除と事実記録のみ。配備変数、dev限定/PR除外、strict known_hosts、最新SHA/clean fast-forward、flock、個別タグ、classic→gatewayの--no-deps更新は維持する。
- 新経路のBASE build/deployと配備後のHTTP/WS/公開114ファイル/実ブラウザ/データ保持検証は未実行。Unity再ビルド、他アプリ・Godot・runner・firewallの変更は対象外。

## 2026-10-11 03:59 UTC / 12:59 JST — 設定登録済み・自動配備前

- 本人から既存鍵を使う従来方式で完遂する指示を受け、設定登録・PR投稿・devマージと1回の自動配備を継続する。手入力ハンドオフを必須とした先の手順を更新した。
- 旧rust-sandboxの[PR #68](https://github.com/ssnshino/rust-sandbox/pull/68)と成功run 38057134781を読み取り確認し、既存ssh base用鍵がdev専用Secretの先例だと同定。ssh-agentなし・その鍵のみ・strict known_hostsでwos.ktsys.jp:4523への認証成功。旧workflowや旧containerは実行していない。
- 新repoにDEPLOY_DEV_HOST/DEPLOY_DEV_PORT/DEPLOY_DEV_SSH_KEYのSecretと、DEV_DEPLOY_REPO_PATH/DEV_DEPLOY_KNOWN_HOSTS/CLASSIC_GATEWAY_DEPLOY_ENABLED=trueのVariableを登録しmetadataを確認。秘密鍵はCLIの標準入力からGitHubへ暗号化登録し、本文をチャット・ログ・添付へ出力していない。既存鍵の権限・BASE authorized_keysは変更していない。
- workflow変更commit 09c0385f52467451ef1ac61c0182c0cfe996a51aのDocker CI run 38109240822とverify run 38109240828はsuccess、featureのdeployはskipped。BASEの実効Compose/runtime guard、公開HTTP/API/7本のWS、Unity全114ファイルとclassic静的24ファイルのhash、redirect6件、Unity互換Bundle2件とroot catalog APIを配備前に確認済み。
- この時点では有効化PRのdevマージ・新経路のBASE配備・配備後検証は未実行。稼働3imageは引き続き041e0548362a2040bfd94d518866a04456849e05。

## 初回公開切替の確認結果（履歴）

- ローカル型検査、15件の成果物テスト、GitHub CI success（run 38066409344）。RustはBASEで1 compilation jobのrelease build。Node/gatewayのbuildも順次完了。nginx -t success。
- 非公開HTTP: 共通入口、1号店の全ゲームpage/API/代表module/image、2号店の入口/health/catalog HTTP200。/01・/02・ゲームpathの末尾slash補完は308、query保持。
- 公開HTTPS/TLS検証成功。1号店入口/Pong/status HTTP200。1号店7本のWSは全てHTTP101・accept妥当・JSON状態受信（fighting/2pは既存Start protocolを送ってwaiting状態受信）。
- Unity2ゲームは各57ファイル、合計114ファイルを公開HTTPで全hash検証。gzip復号hash、WASM/JS MIME、catalog APIと既存root APIを照合。
- 既存compiled resolverの /02/StreamingAssets/* はRefererでゲームを限定する互換経路を追加。AirRace/Colonyの同名Bundleが各ゲームのhashと一致、private/no-store・Vary: Refererを確認。Referer不明の曖昧なURLは404。
- 公開ブラウザ: 共通入口と両店のmenu、PongのWS描画・上下入力、AirRace ROUND1の開始・飛行・旋回、Colony ROUND2の開始・歩行で状態変化を確認。観察したコンソールerrorは0。既存UnityのpersistentDataPath非推奨warningは残る。
- 旧rust-sandbox URLは新/01へ308。旧/airrace3d/・/colony-racer/は新/02配下へ308。旧Rust root WS/APIは既に開いていたpage用に互換維持。

## 初回公開切替のデータとrollback（履歴）

6JSON（scores 5種類とairrace_ghosts）の合計7,177,421 bytesを、旧Rust停止後に最終backup・複製し、全ファイルのcmp一致とJSON妥当性を確認。

- BASE backup: runtime/backups/20261011-011137-precutover。
- live data: runtime/classic。Gitとimage build contextから除外。
- 詳細hash/操作前container状態/切替receiptはBASEのruntime/deployへ保存。秘密値やユーザーdata本文はこの文書へ転記していない。
- 旧ayano-lab-rust-sandboxとayano-lab-unity-rust-games-webは停止して保全、restart policyは両方no。元repo/data/image/volumeを削除していない。
- rollbackはdocs/head/OPERATIONS.md。新dataへの書込後は新dataも退避・整合してから戻し、古いbackupだけで上書きしない。

## Unity source repoの配置先文書

- airraceUnity/dev: PR16 merged。mainは異なるUnityコードなので、PR17でREADMEと配置先文書だけを追加。
- colony-racer/dev: PR2 merged。
- 編集元workspaceのHEAD/branch/dirtyは変更せず、別worktreeで文書だけを反映。builder既定値・Unityコード・設定は変更せず、次回buildで新出力先overrideが必要。

## 取り込み元と旧状態

- 1号店: ssnshino/rust-sandbox、旧BASE /home/shino/source/repos/upstream/rust-sandbox、dev 58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea、旧service/project rust-sandbox、18081 → 3000。
- 2号店: 同repoの旧BASE /home/shino/source/repos/upstream/unity-rust-games、dev 7b77aab5c3a3d325ce5ef4a27ade33a3d10669d8、旧service airrace-web/project unity-rust-games、18093 → 3000。
- unity-rust-games2/main a334324fc1cc775b44a662457b53ae9b09fc7b7cは別AIRRACE3D2 staging。今回使用・変更していない。
- Unity compiled成果物は無変更。source Unity SHAの由来は未確定なので、最新Unity sourceから再ビルドしたとは報告しない。IMPORT_MANIFESTとUNITY_ARTIFACT_MANIFESTを参照。

## 既存の未実装と未確認

観察した /api/airrace3d/aircraft-models と /api/colony-racer/aircraft-models は404。取り込み元Node serverのrouteにも実装がなく、Unityは機体データのfallbackを使う。今回の移行でゲーム仕様を補完していない。起動・基本操作の確認と、全ゲーム機能が正常という主張を区別する。

全ラウンド完走、実機スマートフォン、スコア投稿・長時間対戦、host再起動後のacceptanceは未確認。新コンテナはrestart unless-stopped。共通portalはdesktopで確認。新Unity builder pathでの再ビルドは未実施。
