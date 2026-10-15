## 公開採用済み: 2026-10-15 道路網・山地のスマホ用WebGL

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`、配布release／Unity RELEASE_TAG `e36ccaf102ee8494aa0d60d4d347f268114a9924`、Unity image `sha256:36e023b1586b3f7db8d0bce9bbecf629821eb78ee62b3341e21f2f69cc69dada`。Actions run [38742023882](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38742023882) がsuccess、2026-10-15 22:27 JSTにreceipt accepted／adoptionComplete true／exitCode0を確認。公開URLの通常解像度Edge25・WebKit24 checksも合格。実iPhone/Android性能は未測定。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/ 。高架・南/中央/北環状の移動ボタンを追加。既存Actions認証を使うUnity専用自動配備を追加し、公開ブラウザ後にfinalize、失敗時rollbackまで実動作を確認した。classic/gatewayとruntime dataをguardで保持。詳細は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。以下の公開待ち・未実施は各記録時点の履歴。

# 2026-10-15 道路網・山地のスマホ用WebGL

公開候補を準備し、Unity専用Actionsを検証中。accepted receiptはまだなく、公開済みとは扱わない。

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`。5 IC・3環状線/JCT・盛土中央分離帯・距離案内・DEM山地/森林を含む。スマホから高架・3環状線へ移動するボタンを追加。Infrastructure装飾meshのCPUコピーを除き、森林を圧縮。Colliderと原Prefabは保持。

最終r5: Brotli fallback、build成功（0 errors / 55 warnings）、data 92,787,516 bytes。ローカル実Edge 25 checks、WebKit 24 checksが合格。走行・制動・操舵・reset、3地区、高架、3環状線、縦横表示を確認。初期r1 OOMを記録し、最終r5を再検証済み。Windows出力の `network-web-build-r5.json`、`network-web-qa-r5/smoke-edge.json`、`network-web-qa-r5-webkit/smoke-webkit.json` が証拠。実iPhone/Androidの速度・操作は未測定。

AirRace全資産、旧Colony StreamingAssets/TemplateDataは元manifestのSHA256を照合し保持。ソース・配布SHA・稼働image・文書commitは区別する。

既存の自動配備はclassic/gateway限定だった。今回はUnity専用workflowを追加し、既存Actions secrets/varsをそのまま使用する。WindowsにBASE秘密鍵をコピーしない。devへの反映後、既存guarded helperでUnityのみ仮配備し、実公開ブラウザの6操作観測と描画・高架・環状線を確認してからfinalize。失敗時は同receiptのrollbackを行う。classic/gatewayのimage/container、runtime data、鍵、runner、firewallは変更しない。

Windowsでは既存Nodeテスト19/21（symlink EPERM 2件）、Python既存22件中7件が改行/ファイル操作等で例外。Linux CIで正式確認する。新規wrapperテストはローカル2 pass / Linux専用4 skip。ブラウザテストは実機の代替性能評価ではない。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/
更新前文書の正確なGit blobとSHA256は `docs/history/20261015-before-colony-road-network/PRESERVATION_MANIFEST.json`。

## 自動配備の使い方と回線

Unity編集repoのpushだけではWebGLは生成されない。EditorでWebGLをbuildし、この配布repoのColony成果物とmanifestを更新してdevへ反映するとUnity専用workflowが動く。PRは検証だけで秘密鍵を使わない。配備helperや文書だけの更新は再配備を起動しない。手動起動はdevを指定する。

WAN経由の大容量Git取得が20分以上かかった一方、Windows 192.168.1.34→BASE 192.168.1.23の約98MB bundleは約8秒（約11MiB/s）で転送できた。bundle SHA256 f466306c6bcc466def04eb323a792ad21e991476985f8887de184272c5b6d74e と固定Git refを検証してobjectだけ取り込んだ。臨時LAN serverは停止済み。今後の通常WAN取得に30分の上限と進捗、SSH keepaliveを設け、job全体は60分を確保する。

GPUなしCIの初回検証は開始buttonの30秒timeoutで失敗し、実rollbackが成功した。通常解像度でのsoftware rendererはローカルで約0.3〜0.5fpsを観測。最終CIは実ページのframebufferのみ長辺256pxで検証し、スマホサイズのUIと実操作を保持。実機性能検証として扱わない。最終CIの6観測と12 checks、および通常GPUの公開Edge25/WebKit24を区別する。

accepted receipt: runtime/deploy/unity-colony-e36ccaf102ee8494aa0d60d4d347f268114a9924-20261015T132242Z。正本のActions artifactは unity-colony-release-e36ccaf102ee8494aa0d60d4d347f268114a9924（artifact11976454093）。Windows出力 network-web-public-ci-accepted、network-web-public-edge、network-web-public-webkit にraw記録を保存。
