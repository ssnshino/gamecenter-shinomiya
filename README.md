# gamecenter-shinomiya

ゲームセンターしのみ屋の公開入口、1号店のRustゲーム、2号店のUnity WebGL配布をまとめるリポジトリ。

2026-10-11 JST: BASEへの統合公開に続き、[PR #3](https://github.com/ssnshino/gamecenter-shinomiya/pull/3)をdevへマージしてclassic/gatewayを1回自動配備。[build/deploy run 38110443542](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443542)と[verify run 38110443571](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443571)は成功。公開HTTP・WebSocket・配布hashとMacブラウザの起動・基本操作を確認した。

稼働release SHAはclassic/gatewayがa45dc158dbe1785d971e597ec16d95fe9e77bd4e、Unityが041e0548362a2040bfd94d518866a04456849e05。Unityのimage/container・114ファイルとruntime6JSONを保持した。既存dev用鍵を使う従来方式で接続設定を登録済み。配備後に見つけたSSH標準入力の問題は[PR #4](https://github.com/ssnshino/gamecenter-shinomiya/pull/4)で修正し、未実行だったhealth確認と個別タグ記録は再配備せず補完済み。修正・文書commitと稼働image SHAを区別する。詳細は[現在地](snapshot/CURRENT_SNAPSHOT.md)と[運用手順](docs/head/OPERATIONS.md)を参照。

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

## 旧設計・履歴資料と復元入口

旧資料は以下の元repoとGoogle Driveに保全している。この統合repoへ旧資料一式をコピーした状態ではない。受領件数は各manifestの登録件数で、同じ文書の重複を除いた数ではない。

- GameCenter（受領37件）: [旧repo README](https://github.com/ssnshino/rust-sandbox/blob/dev/README.md) / [受領manifest](https://github.com/ssnshino/rust-sandbox/blob/dev/docs/history/2026-10-10-received/MANIFEST.json) / [設計・仕様・作業ログ](https://github.com/ssnshino/rust-sandbox/tree/dev/docs/history) / [旧計画](https://github.com/ssnshino/rust-sandbox/tree/dev/plan/history) / [旧snapshot](https://github.com/ssnshino/rust-sandbox/tree/dev/snapshot/history) / [GD受領保管](https://drive.google.com/drive/folders/12WX_XviuLWFAsVneXv5WWjoV91RffFKd) / [GD恒久復元manifest](https://drive.google.com/file/d/1-VFe5WFgTk7FfVRnZz3TPbqSrOSJIzUB/view)
- AirRace（受領21件）: [編集元README](https://github.com/ssnshino/airraceUnity/blob/dev/README.md) / [受領manifest](https://github.com/ssnshino/airraceUnity/blob/dev/docs/history/2026-10-10-received/MANIFEST.json) / [設計・仕様・作業ログ](https://github.com/ssnshino/airraceUnity/tree/dev/docs/history) / [旧計画](https://github.com/ssnshino/airraceUnity/tree/dev/plan/history) / [旧snapshot](https://github.com/ssnshino/airraceUnity/tree/dev/snapshot/history) / [GD受領保管](https://drive.google.com/drive/folders/1etPU_9kSnpkP_MD8LhfCad14ApextNm3) / [GD恒久復元manifest](https://drive.google.com/file/d/15z__yY-43GpJ7etITNgMK9AtgKGaYGDP/view)
- Colony Racer（受領3件）: [編集元README](https://github.com/ssnshino/colony-racer/blob/dev/README.md) / [受領manifest](https://github.com/ssnshino/colony-racer/blob/dev/docs/history/2026-10-10-received/MANIFEST.json) / [旧仕様・作業ログ](https://github.com/ssnshino/colony-racer/tree/dev/docs/history) / [GD受領保管](https://drive.google.com/drive/folders/1BBezWlEpVaWrOZ7TaqI9hAwDMqjwDDL-) / [GD恒久復元manifest](https://drive.google.com/file/d/1KvDMYYskC2KDRyt-9xRQAbpAzF_G0yrb/view)

AirRaceの受領21件には変換済みコピー2件が含まれる。原文一致とは扱わず、manifestの変換記録を確認する。GDの保存資料には草案も含まれるため、現在の配布・運用は本repoのsnapshotとdocs/headを優先する。GDへのアクセスは既存の権限に従う。

2026-10-11: 元repoの文書tree、受領manifestの件数、GD保管フォルダの存在を確認。今回は全ファイルのhash再照合や復元試験は行っていない。旧文書のbranch・配置・deploy手順は履歴であり、そのまま実行しない。
