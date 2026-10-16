# スマホ照明修正版の公開結果

照明修正版を公開採用。Unity source `937b98ac785d59354c61c1a3299caaac867a8455`、配布release/Unity RELEASE_TAG `40db65b345aea1ee025b8d83b5d858e4c216c4a9`。Actions run38853563393 success、公開10checks/6operations PASS、receipt accepted/adoptionComplete true/exitCode0、retryRequired/mixedCheckout false。実iPhoneの再確認は待ち。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=lighting-20261016 。軽量でも対応デバイスはHDR/Neutralトーンマップを保持、AOはOFF。Web主光0.85、影強度0.60、露出0、ミラー受光0.15。影距離45/100mとLOD・物理は維持。高速道路/環状線/IC/JCT・N/S長距離道路・山/追加地形・森林は引き続きオミット、コード/元データ保持。

元Scene/Prefab hash不変、Infrastructure767mesh/482collider/3,325,408 summed verticesは起動成功版と同一。data57,353,448bytes/展開後100,944,814bytes。AirRace・旧StreamingAssets/TemplateDataはmanifest照合で保持。ローカルEdge27/WebKit26 PASS。同一視点の遠方路面190x40pixelの白画素率81.26%→0%。PCスクリーンショット比較であり実iPhoneの性能・見え方の証明ではない。

復元先: 市街地切り分け版8c0b9e52590ad0ff00c534f55522012bc278579e（実iPhone17起動・走行済み）、full版f75d8649bb6112326355c45b26f91bd66265f228。Windows EditorのPlay初期化は別件として未検証、Webの走行PASSに読み替えない。

## 受入れ証拠

Actions38853563393のartifactとWindows outputs/lighting-web-public-ci-acceptedを正本とする。公開ブラウザはsoftware framebuffer長辺256pxで性能評価には使わない。通常解像度Edge27/WebKit26はoutputs/lighting-web-edge、outputs/lighting-web-webkit。同一視点比較はoutputs/mobile-lighting-ab-r2、outputs/mobile-lighting-after-r1、outputs/mobile-lighting-comparison.json。

## 実装時の記録

# スマホ照明の修正候補（2026-10-16）

市街地切り分け版はiPhone 17で起動・実走できた。ユーザー写真では近景が青暗く、遠方が白飛びする。軽量/詳細の切替でも変わらないとユーザー確認。基準release 8c0b9e52590ad0ff00c534f55522012bc278579eを復元先に保持する。

Unity source 937b98ac785d59354c61c1a3299caaac867a8455。軽量でも対応デバイスはHDRとNeutralトーンマップを保ち、AOはOFF。HDR非対応はLDRグレーディング。Web主光1.25→0.85、影強度0.82→0.60、露出+0.35→0、ミラー受光0.50→0.15。影距離45/100m、解像度、LOD、物理は維持。

高速道路/環状線/IC/JCT・N/S長距離道路・山/追加地形・森林は引き続き生成しない。city-diagnosticで起動できた範囲を保つ。コードと元データは保持されfullで復帰できる。公開された旧full版f75d8649bb6112326355c45b26f91bd66265f228もGitから復元可能。

基準版の同一視点A/Bでは影OFFで手前まで白飛びし、bias変更/AO切替では主症状が変わらなかった。境目の正確な物理原因の断定ではない。HDRは描画バッファの負担を追加するため、実iPhoneで起動と見え方の再確認が必要。

検証・配備の結果は後記。現時点では候補であり、accepted receiptと実機再確認は未取得。Windows EditorのPlay検証とWeb検証は区別する。

## ビルド・比較

Unity 6000.4.3f1 / native gzip / ETC2 / DiskSizeLTO。Succeeded、errors0、warnings320（旧API等を含む）。Infrastructure 767mesh / 482collider / 3,325,408 summed verticesは起動成功版と一致し、元Scene/Prefab hashも不変。data 57,353,448bytes / 展開後100,944,814bytes（基準57,351,365 / 100,916,295）。WASM 6,936,156 / 19,982,037bytes。AirRace全資産・旧StreamingAssets/TemplateDataをmanifestで照合し保持。

ローカルEdge 27条件PASS。軽量HDR/grade、AO OFF、主光0.85/ミラー0.15、縦横UI、3地区、加速・制動・操舵・reset/pause/resumeを確認。遠方路面の白飛びが抑えられたスクリーンショットあり。WebKitも26条件PASS。同一視点A/Bは検証中。実機の性能・見え方をPCでの結果に読み替えない。
