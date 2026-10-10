# gamecenter-shinomiya

ゲームセンターしのみ屋の公開入口、1号店のRustゲーム、2号店のUnity WebGL配布をまとめるリポジトリ。

2026-10-11 JST: BASEへの統合配置と公開切替を完了。1号店・2号店のHTTPS、配布物、API、WebSocket、ブラウザ起動・基本操作を検証済み。実行release SHAは041e0548362a2040bfd94d518866a04456849e05。詳細はsnapshot/CURRENT_SNAPSHOT.mdを参照。

| 公開先 | 用途 |
|---|---|
| `https://unity-games.wos.ktsys.jp/` | 共通入口 |
| `https://unity-games.wos.ktsys.jp/01/` | 1号店: Rust/axumゲーム |
| `https://unity-games.wos.ktsys.jp/02/` | 2号店: Unityゲーム |
| `https://unity-games.wos.ktsys.jp/02/airrace3d/` | AirRace3D |
| `https://unity-games.wos.ktsys.jp/02/colony-racer/` | Colony Racer |

配布repoは `ssnshino/gamecenter-shinomiya`。Unity編集ソースは `ssnshino/airraceUnity` と `ssnshino/colony-racer` に残し、ビルド済み配布物と配信サーバーをここへ集約する。

再開順: [AGENTS.md](AGENTS.md) → [現在地](snapshot/CURRENT_SNAPSHOT.md) → [統合計画](plan/01_GAMECENTER_INTEGRATION.md) → [Unity配置先](docs/head/UNITY_DELIVERY_CONTRACT.md)。

ローカル標準配置: `/Volumes/SSD250GBUSB/source/repos/upstream/gamecenter-shinomiya`。
BASE配置先: `/home/shino/source/repos/upstream/gamecenter-shinomiya`。共通gatewayの検証ポートは127.0.0.1:18094。

1号店の取り込み元は、BASEで確認した旧 `rust-sandbox/dev` の `58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea`。2号店は `rust-sandbox/dev` の `7b77aab5c3a3d325ce5ef4a27ade33a3d10669d8`。現在の `rust-sandbox/dev` を1号店の復元元にしない。


開発/配備手順: [運用手順](docs/head/OPERATIONS.md)。Unity再ビルドはこのrepoでは行わず、編集元で新出力先を指定して成果物を取り込む。
