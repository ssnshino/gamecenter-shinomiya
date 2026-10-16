# Safariダブルタップ拡大の対策候補

ユーザーのiPhone写真は軽量固定・113.4km/h・30fps。体感改善の報告と、連続タップでページ全体が拡大し操作部がはみ出す報告。

ゲーム全体にtouch-action:manipulation、走行中none。余白/HUDも対象にし、停止メニューのscroll/pinchを維持。Safari補助として350ms/32px以内の単指連続tapのtouchendをcancelし、buttonのclickは明示送信。multi-touch/touchcancelで連続判定をresetし、pointerイベントは止めない。

純Node event動作9条件PASS。CUA実ゲームは起動・品質切替・reset連続クリック・縦横とconsoleを確認。portrait走行中root none、倍率1、console error0。iPhoneのnative double-tapを再現した証拠ではなく、実機再確認が必要。ローカルQAコマンドと記録/Git反映コマンドが自動承認reviewでblocked by policy（理由詳細なし）。前者はCUA/pure event検証に切替、後者はユーザーがGitHub反映と公開を明示承認。

CSS/JS以外のartifact inventoryとAirRace/保持資産は不変。engine source937b98aの既存data/wasm等を使用し、新Unity buildはしない。影/1エリア化は対象外。公開受入れは未実施。

参考: https://webkit.org/blog/5610/more-responsive-tapping-on-ios/ 、https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/touch-action 。iOS全版を保証しない。
