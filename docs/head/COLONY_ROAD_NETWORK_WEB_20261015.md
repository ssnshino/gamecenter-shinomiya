# 2026-10-15 道路網・山地のスマホ用WebGL

公開候補を準備し、Unity専用Actionsを検証中。accepted receiptはまだなく、公開済みとは扱わない。

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`。5 IC・3環状線/JCT・盛土中央分離帯・距離案内・DEM山地/森林を含む。スマホから高架・3環状線へ移動するボタンを追加。Infrastructure装飾meshのCPUコピーを除き、森林を圧縮。Colliderと原Prefabは保持。

最終r5: Brotli fallback、build成功（0 errors / 55 warnings）、data 92,787,516 bytes。ローカル実Edge 25 checks、WebKit 24 checksが合格。走行・制動・操舵・reset、3地区、高架、3環状線、縦横表示を確認。初期r1 OOMを記録し、最終r5を再検証済み。Windows出力の `network-web-build-r5.json`、`network-web-qa-r5/smoke-edge.json`、`network-web-qa-r5-webkit/smoke-webkit.json` が証拠。実iPhone/Androidの速度・操作は未測定。

AirRace全資産、旧Colony StreamingAssets/TemplateDataは元manifestのSHA256を照合し保持。ソース・配布SHA・稼働image・文書commitは区別する。

既存の自動配備はclassic/gateway限定だった。今回はUnity専用workflowを追加し、既存Actions secrets/varsをそのまま使用する。WindowsにBASE秘密鍵をコピーしない。devへの反映後、既存guarded helperでUnityのみ仮配備し、実公開ブラウザの6操作観測と描画・高架・環状線を確認してからfinalize。失敗時は同receiptのrollbackを行う。classic/gatewayのimage/container、runtime data、鍵、runner、firewallは変更しない。

Windowsでは既存Nodeテスト19/21（symlink EPERM 2件）、Python既存22件中7件が改行/ファイル操作等で例外。Linux CIで正式確認する。新規wrapperテストはローカル2 pass / Linux専用4 skip。ブラウザテストは実機の代替性能評価ではない。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/
更新前文書の正確なGit blobとSHA256は `docs/history/20261015-before-colony-road-network/PRESERVATION_MANIFEST.json`。
