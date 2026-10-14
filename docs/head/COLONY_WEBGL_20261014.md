# Colony Racer 共通WebGL更新 — 2026-10-14

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
