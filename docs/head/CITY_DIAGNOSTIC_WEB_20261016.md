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

# 市街地中心のiPhone起動切り分け版

森林なし公開版でもiPhone 17は開始前に落ちる、とユーザー実機で確認。高速道路/山/N-S方面直線道路を一時的に外し、すぐ復帰できる版を依頼された。今回の公開は診断用であり、iPhone修正成功とは扱わない。

Unity source: d30013583556733cadb80d1cb043af65272c7d5e。`city-diagnostic` をシーンへベイク。生成しない: 軸高架・環状線・IC/JCT・地上長距離道・関連中央分離帯/標識/予約敷地・山/草原/造成地。市街地3地区・元の橋・鉄骨・内壁安全支持・採光帯・街区LOD・街路樹は保持。森林は既存OFF。

通常→診断→再読込→通常復帰PASS。Infrastructure mesh2737→767、Collider7979→482、山/地形89→0、追加道路判定1356→0。鉄骨240/内壁525mesh、市街地4627meshの名前/頂点数/局所位置/scaleの比較hash一致。元のScene/Prefab SHA256保持。

Web Build Succeeded/errors0/warnings286（再コンパイルに伴う既存API非推奨警告等を含む）。native Gzip/fallback false/ETC2/GLES3/DiskSizeLTO、initial256/max1024MB、wasm2023=falseを継続。data配信57,351,365bytes/展開後100,916,295bytes（前便84,612,569/162,904,246）。data decoded SHA256 02d80786f5c22ae50258b0563112dfd8f5680047af7b3a56e70f7c88769fcf32。visual mesh CPU copy除外285、forest compressed0。

ローカルEdge22/WebKit21 checks PASS。開始・3地区・縦横touch・加速/制動/操舵/復帰・省略道路ボタン非表示を確認。CIは明示的なcityDiagnostic telemetry時のみ道路移動の代わりに非表示/無効化を確認し、通常版の道路試験は保持。256px software CIを実機性能の証拠にはしない。AirRace/保持catalog/Bundle/StreamingAssets/TemplateDataの一致をmanifestで確認。

配備は既存のUnity専用Actionsを使い、guard→仮配備→公開ブラウザ→acceptedの順。公開採用済み。release8c0b9e52590ad0ff00c534f55522012bc278579e、Actions38846295459 success。receipt /home/shino/source/repos/upstream/gamecenter-shinomiya/runtime/deploy/unity-colony-8c0b9e52590ad0ff00c534f55522012bc278579e-20261016T033639Z、accepted/adoptionComplete true/exitCode0。公開software browser9checks/6operations PASS、native gzip/MIME確認済み。実iPhoneで開始・走行確認。照明問題は残り次便。URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=city-diagnostic-20261016

復帰: UnityはCOLONY_SCENERY_PROFILE=fullで再生成。Editorメニュー（source follow-up）はColony Racer > Diagnostics > Restore Full Scenery。公開の直前生成済みWebGLはrelease f75d8649bb6112326355c45b26f91bd66265f228に保存済みで、Unity再ビルドなしにGit復元/再配備できる。
