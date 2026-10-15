# Gamecenter Shinomiya

開始順はREADME、snapshot/CURRENT_SNAPSHOT.md、plan/01_GAMECENTER_INTEGRATION.md、docs/head/UNITY_DELIVERY_CONTRACT.md。

- このrepoは配布と配信の統合先。Unity編集ソースはairraceUnityとcolony-racerの各repoに残す。
- 現在地の予定、確認済み事実、実装済み・公開済みを区別する。URLの記載だけで切替済みと扱わない。
- 1号店は旧Rust checkoutの固定SHA、2号店は確認した配布checkoutの固定SHAから取り込む。名称やbranch名だけでゲームを同定しない。
- 初期取り込みで旧deploy workflow、秘密情報、target/node_modules、実ユーザーのスコア・ゴーストデータをコピーしない。元のGit履歴と資料の所在を保存する。
- 既存の1号店・2号店・Unityソース作業場のdirty stateを保護する。計画用作業場の内容を既存作業場へ無条件に上書きしない。
- 2026-10-11: ユーザーの「１号店、２号店公開まですすめて！」で統合実装、ビルド、GitHub反映、BASE配置、対象公開切替を承認。Unity編集ソースの変更・再ビルド、他アプリ操作、データ削除、鍵/firewall/runner変更は範囲外。
- 実装・検証・GitHubへの反映・公開切替は各段階の実施内容を明示する。既存workflowを流用して勝手に配備しない。

