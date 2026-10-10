# 現在地: 2026-10-11 JST

## 合意した方針

- 公開サイト、配信サーバー、ビルド済みゲームをgamecenter-shinomiyaへ集約する。
- 1号店は `/01/`、2号店は `/02/`。Unity編集ソースは既存2repoに残す。
- Unity repoへ新しい配置先情報を記載する。

## 完了した準備

- ローカルrepoをdevで初期化し、移行計画と配置先契約を作成した。GitHub repoは未作成。
- Unity両repoの最新GitHub devを取得し、元作業場を変えず文書用worktreeを作成した。
- URL、API、WebSocket、Unity builderの出力先上書きを読み取り確認した。

## 実稼働の確認点

- 1号店: BASE `/home/shino/source/repos/upstream/rust-sandbox`、dev `58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea`、container `ayano-lab-rust-sandbox`、service/project `rust-sandbox`、18081 → 3000。既存containerを起動し、HTTP200とWS101・ゲーム状態受信を確認済み。
- 2号店: BASE `/home/shino/source/repos/upstream/unity-rust-games`、origin `ssnshino/rust-sandbox`、dev `7b77aab5c3a3d325ce5ef4a27ade33a3d10669d8`、container `ayano-lab-unity-rust-games-web`、service `airrace-web`、project `unity-rust-games`、18093 → 3000。読み取り確認のみ。
- `unity-rust-games2/main` `a334324fc1cc775b44a662457b53ae9b09fc7b7c` はAIRRACE3D2の別再構築staging。今回の2号店取り込み元ではない。

## 公開GOと実装

2026-10-11: ユーザーが「１号店、２号店公開まですすめて！」と指示。新repoのコード、成果物、3service Compose、gateway、/01ブラウザpath、/02互換APIを実装。ローカル型検査、15件の成果物テスト、2ゲーム全配布物hash検証を通過。旧Unityビルド成果物は無変更。

## 残作業

GitHub作成・反映、BASEでの順次imageビルド、非公開ポートQA、データ退避/引継、公開切替、画面操作、Unity2repoの文書反映。旧repo/container/dataはrollback用に保全し廃止しない。

再開はplan/01_GAMECENTER_INTEGRATION.mdから。既存URLが動いていることと新URLで動くことを混同しない。

