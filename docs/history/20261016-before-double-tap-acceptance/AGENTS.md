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

# Gamecenter Shinomiya

開始順はREADME、snapshot/CURRENT_SNAPSHOT.md、plan/01_GAMECENTER_INTEGRATION.md、docs/head/UNITY_DELIVERY_CONTRACT.md。

- このrepoは配布と配信の統合先。Unity編集ソースはairraceUnityとcolony-racerの各repoに残す。
- 現在地の予定、確認済み事実、実装済み・公開済みを区別する。URLの記載だけで切替済みと扱わない。
- 1号店は旧Rust checkoutの固定SHA、2号店は確認した配布checkoutの固定SHAから取り込む。名称やbranch名だけでゲームを同定しない。
- 初期取り込みで旧deploy workflow、秘密情報、target/node_modules、実ユーザーのスコア・ゴーストデータをコピーしない。元のGit履歴と資料の所在を保存する。
- 既存の1号店・2号店・Unityソース作業場のdirty stateを保護する。計画用作業場の内容を既存作業場へ無条件に上書きしない。
- 2026-10-11: ユーザーの「１号店、２号店公開まですすめて！」で統合実装、ビルド、GitHub反映、BASE配置、対象公開切替を承認。Unity編集ソースの変更・再ビルド、他アプリ操作、データ削除、鍵/firewall/runner変更は範囲外。
- 実装・検証・GitHubへの反映・公開切替は各段階の実施内容を明示する。既存workflowを流用して勝手に配備しない。

