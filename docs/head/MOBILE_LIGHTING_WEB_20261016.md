# スマホ照明の修正候補（2026-10-16）

市街地切り分け版はiPhone 17で起動・実走できた。ユーザー写真では近景が青暗く、遠方が白飛びする。軽量/詳細の切替でも変わらないとユーザー確認。基準release 8c0b9e52590ad0ff00c534f55522012bc278579eを復元先に保持する。

Unity source 937b98ac785d59354c61c1a3299caaac867a8455。軽量でも対応デバイスはHDRとNeutralトーンマップを保ち、AOはOFF。HDR非対応はLDRグレーディング。Web主光1.25→0.85、影強度0.82→0.60、露出+0.35→0、ミラー受光0.50→0.15。影距離45/100m、解像度、LOD、物理は維持。

高速道路/環状線/IC/JCT・N/S長距離道路・山/追加地形・森林は引き続き生成しない。city-diagnosticで起動できた範囲を保つ。コードと元データは保持されfullで復帰できる。公開された旧full版f75d8649bb6112326355c45b26f91bd66265f228もGitから復元可能。

基準版の同一視点A/Bでは影OFFで手前まで白飛びし、bias変更/AO切替では主症状が変わらなかった。境目の正確な物理原因の断定ではない。HDRは描画バッファの負担を追加するため、実iPhoneで起動と見え方の再確認が必要。

検証・配備の結果は後記。現時点では候補であり、accepted receiptと実機再確認は未取得。Windows EditorのPlay検証とWeb検証は区別する。

## ビルド・比較

Unity 6000.4.3f1 / native gzip / ETC2 / DiskSizeLTO。Succeeded、errors0、warnings320（旧API等を含む）。Infrastructure 767mesh / 482collider / 3,325,408 summed verticesは起動成功版と一致し、元Scene/Prefab hashも不変。data 57,353,448bytes / 展開後100,944,814bytes（基準57,351,365 / 100,916,295）。WASM 6,936,156 / 19,982,037bytes。AirRace全資産・旧StreamingAssets/TemplateDataをmanifestで照合し保持。

ローカルEdge 27条件PASS。軽量HDR/grade、AO OFF、主光0.85/ミラー0.15、縦横UI、3地区、加速・制動・操舵・reset/pause/resumeを確認。遠方路面の白飛びが抑えられたスクリーンショットあり。WebKitも26条件PASS。同一視点A/Bは検証中。実機の性能・見え方をPCでの結果に読み替えない。
