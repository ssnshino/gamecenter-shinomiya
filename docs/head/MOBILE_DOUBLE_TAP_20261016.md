<!-- MOBILE_DOUBLE_TAP_ACCEPTED_START -->
## 現在: ダブルタップ拡大防止版を公開（2026-10-16）

配布release/Unity RELEASE_TAG `004110fd8efd70e1a5890608b8f0cb92a5a36e88`。Actions38863673644 success、公開実ゲーム10checks/6operations PASS、receipt accepted/adoptionComplete true/exitCode0、retryRequired/mixedCheckout false。Web template source fb9df73eb723ed5661ea973bc83c5f8027bd44fe。Unity engine source937b98aの既存buildを使用し、今回Unity再buildはしていない。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=double-tap-20261016 。ゲーム全体にtouch-action、Safariの近接連続tap補助を追加。2本指入力を連続tap判定から除き、button連続操作を保持。純Nodeイベント9条件PASS、CUA実ゲームの起動・品質切替・連続reset・縦横表示/倍率1・console error0を確認。実iPhoneのnative zoom解消はユーザー再確認待ち。

前版はユーザーが軽量化を体感し30fps表示を報告（持続性能測定ではない）。スマホ軽量固定を維持。市街地の影は未解決、1エリアCore重視は相談段階。詳細はdocs/head/MOBILE_DOUBLE_TAP_20261016.md。更新前文書はdocs/history/20261016-before-double-tap-acceptanceへexact bytes/hashで保存。以下は各時点の履歴。
<!-- MOBILE_DOUBLE_TAP_ACCEPTED_END -->

# Safariダブルタップ拡大の対策候補

ユーザーのiPhone写真は軽量固定・113.4km/h・30fps。体感改善の報告と、連続タップでページ全体が拡大し操作部がはみ出す報告。

ゲーム全体にtouch-action:manipulation、走行中none。余白/HUDも対象にし、停止メニューのscroll/pinchを維持。Safari補助として350ms/32px以内の単指連続tapのtouchendをcancelし、buttonのclickは明示送信。multi-touch/touchcancelで連続判定をresetし、pointerイベントは止めない。

純Node event動作9条件PASS。CUA実ゲームは起動・品質切替・reset連続クリック・縦横とconsoleを確認。portrait走行中root none、倍率1、console error0。iPhoneのnative double-tapを再現した証拠ではなく、実機再確認が必要。ローカルQAコマンドと記録/Git反映コマンドが自動承認reviewでblocked by policy（理由詳細なし）。前者はCUA/pure event検証に切替、後者はユーザーがGitHub反映と公開を明示承認。

CSS/JS以外のartifact inventoryとAirRace/保持資産は不変。engine source937b98aの既存data/wasm等を使用し、新Unity buildはしない。影/1エリア化は対象外。公開受入れは未実施。

参考: https://webkit.org/blog/5610/more-responsive-tapping-on-ios/ 、https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action 。iOS全版を保証しない。
