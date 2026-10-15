<!-- IOS_SAFARI_BOOT_START -->
## 現在: iPhone Safariの起動クラッシュに対応（2026-10-15）

ユーザー実機でSafariが繰り返しクラッシュした。PC/WebKit smoke合格をiPhone適合と扱わない。対策版公開済み・iPhone実機の解消は未確認。約93MB→219MBのJS Brotli展開を、ブラウザnative展開へ変更。圧縮byte・展開後byteとUnityゲーム内容は同一。JS/WASMの.br MIMEを補正し、通常Edge/WebKitの確認を行った。機種・落ちる段階は確認待ち。原因はメモリ不足の可能性があり、断定していない。

詳細と公開receiptは `docs/head/IOS_SAFARI_BOOT_20261015.md`。以前の公開受入れはPC/ソフトウェアブラウザでの受入れであり、iPhone起動成功の証拠ではない。
<!-- IOS_SAFARI_BOOT_END -->

## 公開採用済み: 2026-10-15 道路網・山地のスマホ用WebGL

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`、配布release／Unity RELEASE_TAG `e36ccaf102ee8494aa0d60d4d347f268114a9924`、Unity image `sha256:36e023b1586b3f7db8d0bce9bbecf629821eb78ee62b3341e21f2f69cc69dada`。Actions run [38742023882](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38742023882) がsuccess、2026-10-15 22:27 JSTにreceipt accepted／adoptionComplete true／exitCode0を確認。公開URLの通常解像度Edge25・WebKit24 checksも合格。実iPhone/Android性能は未測定。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/ 。高架・南/中央/北環状の移動ボタンを追加。既存Actions認証を使うUnity専用自動配備を追加し、公開ブラウザ後にfinalize、失敗時rollbackまで実動作を確認した。classic/gatewayとruntime dataをguardで保持。詳細は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。以下の公開待ち・未実施は各記録時点の履歴。

## 2026-10-15 Unity自動配備の追加（検証・公開待ち）

今回のスマホ向けデプロイ依頼と自動配備の確認を受け、Unity専用 `.github/workflows/deploy-unity-web.yml` を追加。dev更新で既存Actions認証を利用し、Unity限定仮配備、実公開ブラウザでの起動・運転確認、finalizeの順に進め、受入れ失敗時はrollbackする。classic/gateway workflow、鍵、runner、firewallは変更しない。以下の旧作業範囲は記録当時のもの。現在の証拠は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md` に記録し、accepted receipt確認まで公開完了と扱わない。

# Gamecenter Shinomiya

開始順はREADME、snapshot/CURRENT_SNAPSHOT.md、plan/01_GAMECENTER_INTEGRATION.md、docs/head/UNITY_DELIVERY_CONTRACT.md。

- このrepoは配布と配信の統合先。Unity編集ソースはairraceUnityとcolony-racerの各repoに残す。
- 現在地の予定、確認済み事実、実装済み・公開済みを区別する。URLの記載だけで切替済みと扱わない。
- 1号店は旧Rust checkoutの固定SHA、2号店は確認した配布checkoutの固定SHAから取り込む。名称やbranch名だけでゲームを同定しない。
- 初期取り込みで旧deploy workflow、秘密情報、target/node_modules、実ユーザーのスコア・ゴーストデータをコピーしない。元のGit履歴と資料の所在を保存する。
- 既存の1号店・2号店・Unityソース作業場のdirty stateを保護する。計画用作業場の内容を既存作業場へ無条件に上書きしない。
- 2026-10-11: ユーザーの「１号店、２号店公開まですすめて！」で統合実装、ビルド、GitHub反映、BASE配置、対象公開切替を承認。Unity編集ソースの変更・再ビルド、他アプリ操作、データ削除、鍵/firewall/runner変更は範囲外。
- 実装・検証・GitHubへの反映・公開切替は各段階の実施内容を明示する。既存workflowを流用して勝手に配備しない。

