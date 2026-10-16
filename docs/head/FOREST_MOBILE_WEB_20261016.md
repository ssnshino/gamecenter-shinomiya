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

# 森林なし・街区LOD版のWeb公開採用（2026-10-16）

ユーザーのスマホ再試走用デプロイ依頼で公開。旧native Brotli版はiPhone 17で開始前クラッシュしたが、今回の実iPhoneはまだユーザー検証待ち。

Unity source: a02c3ae8909e02084a2d44ee7fb2ab6aa19cebc8。森林を省き遠景街区LODを加えたruntimeはd1502bcと同一。EditorだけにCOLONY_WEB_COMPRESSION=native-gzipを追加。Build Succeeded/errors0/warnings22、元Scene/Prefab hash保持、ETC2/GLES3/DiskSizeLTO、wasm2023=false、initial256/max1024MB。森林mesh0。元作業場の材質6ファイルの実行時keyword差分とPackages2差分は保持し、ビルドコピーの材質はcommitのbyteで固定した。

配布release/Unity RELEASE_TAG: f75d8649bb6112326355c45b26f91bd66265f228、PR #15。Actions run https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38836767257 はsuccess。receiptは `/home/shino/source/repos/upstream/gamecenter-shinomiya/runtime/deploy/unity-colony-f75d8649bb6112326355c45b26f91bd66265f228-20261016T014548Z`、phase=accepted/adoptionComplete=true/exitCode=0、previousCheckout=db6b78b7631800b6b16fa9bcb6ba4239eda84a7e。rollbackは不要でskipされた。classic/gatewayと永続data、AirRace全fileと保持StreamingAssets/TemplateDataは既存guardで照合保持。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=forest-20261016 。indexのCache-Control max-age=300のため試走用queryを付けた。data84,612,569bytes→HTTP展開162,904,246bytes。前便native Brotliは92,787,516→218,766,927bytes。Wasm gzip6,934,787→19,979,554bytes。公開HEADは3圧縮fileともContent-Encoding:gzip、JS/WASM MIMEが適正。Content-LengthはHEADに無く、それをエラーとせずCIの実GET展開後hashで検証した。

Brotli初回はWASMリンクまで完了したがdata圧縮が20分超・入力約半分で、検証した自分の隔離brotli workerだけを停止した。失敗reportは残し、元Scene/Prefabの復元を確認。gzip level6比較は163,060,694→86,233,107bytes/35.44秒で、100MiB制限内だったため正式Gzip profileで再ビルドし成功。画像/decoded contentを変える品質設定変更ではない。初回Brotliを成功版と数えない。

ローカルEdge25・WebKit24 checks PASS、公開通常解像度WebKit24 checks PASS。公開CIの12checksと6operations（load/districts/accelerate/brake/reset/pause）もPASS。CIはUIをphone寸法にするがframebuffer長辺256pxのsoftware WebGLであり、スマホ実機/FPS/メモリの保証ではない。今回物理設定や道路/JCTを変更せず、元の森林省略で幾何hash保持と中央環状520m接地喪失0が検証済み。今回Web smokeは限定した道路/地区移動/加速/制動で、JCT全ランプ実走を繰り返したものではない。

前回遅かったWAN経由のGit object転送は、SHA-256を固定した89,307,806byte bundleをPC192.168.1.34からBASE192.168.1.23へLAN転送し、専用refs/remotes/colony-lan/forest-mobile-20261016へfetchして交渉に再利用。prefetch run38836631644成功、checkout/servicesは変更しなかった。鍵/runner/firewallの追加変更なし。LAN serverとlocal test serverは停止済み。実デプロイは既存dev Actions/guard/finalize経路。

証拠: このPCの C:/Users/shino/Documents/Codex/2026-10-15/c/outputs/forest-web-publication.json、forest-web-source-inventory.json、forest-web-gzip-build.json、forest-web-build-brotli-failed.json、forest-web-transport.json、forest-web-public-headers.json、forest-web-edge/、forest-web-webkit/、forest-web-public-webkit/、forest-web-public-ci-accepted/。artifact12019342885のZIP SHA-256はc9497a75b79d911924d0c9809e59cd92ea18737f148d533c6d9fd819e9765927。source code commit、distribution release、docs-only commitを区別する。配備guardは実imageの一致を確認したが、この取得artifactにimage IDの単独台帳は無く、推測で記載しない。
