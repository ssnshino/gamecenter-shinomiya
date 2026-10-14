# Colony Racer 共通WebGL更新 — 2026-10-14

## 完了（入力・描画prototype公開）: 2026-10-14 Colony Racer共通WebGL

既存Core／East／West、固定躯体・生活街区とP0-P2車体を、[https://unity-games.wos.ktsys.jp/02/colony-racer/](https://unity-games.wos.ktsys.jp/02/colony-racer/) のPC・タッチ共通版へ更新した。PCはW／Space／A・D、スマホは左のアナログ操舵・右の加速と制動。旧公開版にぷにこんがあったという推測は本人確認で訂正し、新しいtouch controllerを採用した。スマホ専用Sites案は中止・未公開。

2026-10-14 23:51 JSTに公開採用を完了した。配布devと永続Unity RELEASE_TAGは `91efbec9032aaa087236e0965d7e0cb16b9ff583`、Unity sourceは `ab3394504e39b7997eeb1e454f82bfb55088ffef`、Unity imageは `sha256:48d91a6cb4d99dc0ff890ad9c63e817e88e59df43ac7c7e05e357933aae4fea6`。accepted receipt／BASE clean checkout／公開PC24checks・touch33checks計528samples／post-final115file hash・gzip・MIME・catalog APIのexit0を照合した。今回の採用は共通controller／render prototypeの公開で、接地安定の受入れとは分ける。

独立 `public-acceptance-audit.json` の7群PASSで同Unity image、対象外132container、runtime6JSON、routing／Compose／gateway設定、AirRace57file、既存Colony StreamingAssets37／TemplateData14を照合した。classic／gatewayはa45dc158のimage／containerを継続し、gatewayはDNS再解決のgraceful reloadだけを行った。runtime dataをGitへ取り込んでいない。

Webの入力・描画smokeと連続接地を区別する。ローカル3環境の88checks／807samplesはsmoke PASS、100km/h以上の近傍路面でcontactが間欠的に外れるため連続接地gateはfalse。motor・操舵はcontactでgateされるのでHUDだけの問題とは扱わない。iPhone hardware・実機fpsは未測定。Native r9の115条件は履歴で、WebGL合格へ転記しない。

結果は [Colony WebGL更新](../../docs/head/COLONY_WEBGL_20261014.md)、手順は [Unity限定公開](../../docs/head/COLONY_WEBGL_PUBLICATION.md)。source commit・配布commit・image SHA・実URLを別に照合して再開する。以下は更新前の記録で、旧Unity image041e054と『再ビルド／公開未実施』は各記録時点の履歴。

### 今回の採用結果

| 公開URLの逐次再測定 | 入力・描画 | 120km/h目標 → 制動後 | samples |
| --- | --- | --- | --- |
| Chromium PC r2 | 24checks PASS | 119.993439 → 0.00840356km/h | 299 |
| Chromium touch r2 | 33checks PASS | 118.362396 → 0.01754934km/h | 229 |

表はaccelerate120という点測定と制動後の値。touchの点測定は118.362396km/h、同runの別sampleで最大119.994598km/hを記録した。点測定と最大値を分け、2%速度gateで評価する。

公開PC r2の100km/h以上の直進加速は23samples中10、touch r2は14samples中4でcontact false、probe miss0、自動復帰0。連続接地は入力・描画smokeの受入れと別にfalseとして残す。これはrender機会の観測で、50Hz全tickの記録ではない。runtime console error／page error／failed requestは各0、Chromium起動warning各6は保持する。

初回公開browser suite2件は不合格としてRAWに保持した。PCはWest画面のPNG保存でfont待ち30秒timeout、touchは旧catalog6requestのERR_ABORTED。並行GPU実行の影響は仮説であり、途中のcontroller／描画成功だけでsuiteを合格にしない。採用対象は順次再実行した最終suiteとaccepted receiptである。

[配布dev commit](https://github.com/ssnshino/gamecenter-shinomiya/commit/91efbec9032aaa087236e0965d7e0cb16b9ff583) を固定してUnityだけを更新した。`public-accepted-receipt.json` のphase accepted／postFinalPublicSmoke exit0、`public-browser-acceptance.json` のcontroller／render scope、`public-acceptance-audit.json` の7群PASSが採用根拠。BASE receiptは `runtime/deploy/unity-colony-91efbec9032aaa087236e0965d7e0cb16b9ff583-20261014T143235Z`。source／配布／稼働SHAを区別する。

停止点は公開採用。contactの残課題と実iPhone未確認を引き継ぐ。`helper-stop-complete.json` は内部Editor3180と検証server12184の不在・port8364閉鎖を確認した。既知rollback image041e054は保持しているが、accepted後の復旧は現在のcheckout・tags・dataを再照合して判断する。

以下はビルド・ローカル検証・公開前commitと初回guard停止の保存記録。今回の最終採用は上の新しいproofで判断し、過去の『公開切替は未実施』を現在の状態へ転記しない。

既存Core／East／Westの固定躯体・生活街区とP0〜P2車体を、従来の https://unity-games.wos.ktsys.jp/02/colony-racer/ へ配布する。PCはキーボード、タッチ端末は左アナログ操舵と右加速・制動を表示する。旧公開版にタッチパッドがあるという推測は本人の確認で訂正し、新しい操作を追加した。スマホ専用Sites案は中止し、配信していない。

このcommit時点はビルド・ローカル確認済み、公開切替は未実施。公開完了はaccepted receiptと実公開ブラウザ記録で別途示す。

## ビルドと保持

Unity編集元のlocal commitは `ab3394504e39b7997eeb1e454f82bfb55088ffef`。Unity 6000.4.3f1 ARM64／WebGL、GLES3／ETC2／Gzip＋decompression fallback／Medium stripping／DiskSizeLTO。最終buildは2026-10-14 13:42:19 UTC、Succeeded、errors0／warnings221。warningsは既存missing attached script213、既存CS0618の7種類、Editor Pipeline runtime無効化通知1。未解消警告を0と扱わない。

SourceIdは `d7179553bb9e3bd962add4f3b143982a19dc021f+web-e64b2c9c056b57d045622406ee7af40362226b0c634af2c2160f363e2a5c4909`。830 sourceのGit blob／disk／frozen、実package1817／build settings22を別々に照合した。元scene／prefabとP0保護9sourceを保持し、物理は50Hz／Discreteのまま。WebGL専用分岐で反射を所有ARGB32 cube RenderTextureへ変更し、GPU CopyTexture非対応と縮小mipのdepth寸法不一致を避けた。飛行機モデルは既存built-in defaultを使い、存在しないAPI／fileへの取得を止めた。Nativeコード分岐は保持する。

Colony配布58ファイル計57,961,232bytes。AirRace57全ファイル、旧Colony StreamingAssets37／TemplateData14をbyte保持し、全2ゲーム115ファイルのHTTP hash／gzip・MIME／catalog APIをローカルの実Nodeサーバーで照合した。新生成wrapperとBuildだけを更新する。Unity runtimeのEditor Pipelineサーバーを有効にしていない。

## 実ブラウザ確認と制限

Mac Apple M2のtask-owned headlessブラウザで実際のcompiled Unityを動かした。Chromium151.0.7922.34のPC24条件／touch33条件、WebKit26.5のtouch31条件はcontroller・描画smoke PASS。telemetryはそれぞれ348／225／228 samples。実GPUはChromium ANGLE Metal Apple M2、WebKit Apple GPU。

PC入力、アナログ半量・全量・deadzone、加速併用、独立した指の解放、CDPのtrusted2-contact touch／cancel、制動、reset、3地区、視点、停止、品質切替、縦横の非重複配置を確認した。WebKitの同時操作はmouse＋keyboardによるcoarse-pointer emulationで、2本の実touch injectionはChromiumで測った。iPhone実機性能は未測定。headlessでOSのtrusted focus lossが発生しなかったため、blur handlerは明示的にdispatchして確認した。

120km/h目標の2%速度gateでの接地点はPC118.333、Chromium touch119.497、WebKit119.993km/h。制動後0.00572／0.01145／0.00852km/h。加速中の自動復帰は0。ブラウザruntime console error／page error／failed request0。Chromiumの初期format照会warning各6、WebKitのpolygon-mode extension warning1は残る。3地区の反射framebuffer寸法エラーは修正後0。

**連続接地は未達。** 100km/h以上・直進throttleの描画機会でPC17点中9、Chromium touch15点中10、WebKit17点中9がcontactなし。全て近傍road rayはhitし、自動復帰はないが、motor・操舵はcontactでgateされるため、単なるHUDの揺れとは扱わない。過去Native r9の115条件は異なる軌跡の履歴で、WebGLの合格へ転記しない。車線位置での接触・solverの揺れが次の調査候補。今回の公開は操作・描画可能なprototypeの更新であり、接地安定の受入れ完了ではない。

## 公開・復旧

[Unity限定公開手順](COLONY_WEBGL_PUBLICATION.md)に従い、PR→devの固定SHAからUnity imageだけ更新する。classic／gateway image、既存データ、routingは保持し、gatewayはDNS更新のgraceful reloadを行う。暫定公開のHTTP／全hash／API／実ブラウザ成功後だけUnity RELEASE_TAGを保存する。失敗・SSH中断は既知image／タグだけへ限定復旧し、混在checkoutが残る場合は未採用として記録する。

小さいrawは `/Volumes/SSD250GBUSB/source/validation/colony-racer/20261014-mobile-webgl-preview`、大きなEditor・project copy・成果物は `/Users/shino/Library/Caches/ColonyRacerWebGL`。旧候補の失敗記録を保持している。source commit、配布commit、稼働image SHAは区別する。

## 初回公開処理の停止と修正

PR #5のdev merge `721e75ec53bd7134e62efef0011375d521ab38ee` から新Unity image `sha256:48d91a6cb4d99dc0ff890ad9c63e817e88e59df43ac7c7e05e357933aae4fea6` をbuildしたが、切替前の保持guardで停止した。133コンテナの45件がmount一覧の順序だけ異なり、identity／image／StartedAt／state・runtime6JSON・routing／release設定の実変更は0。旧Unity image／公開版を保持した。failed-build receiptは履歴として残す。

比較対象のmountsとDNS aliasesの順序を正規化する修正を追加し、実記録の全133件が一致することを確認した。mount追加／削除／RW変更は引き続き拒否し、保持検査を省略していない。Python29件PASS。修正後のdev固定SHAで公開工程を行い、最終採用は別に記録する。
