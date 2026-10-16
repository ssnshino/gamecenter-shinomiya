<!-- FOREST_WEB_PUBLICATION_START -->
## 現在: 森林なし・遠景街区LODのWebGLを公開採用（2026-10-16）

Unity source `a02c3ae8909e02084a2d44ee7fb2ab6aa19cebc8`（runtimeはd1502bcと同一、Editor native-gzip profile追加）、配布release/Unity RELEASE_TAG `f75d8649bb6112326355c45b26f91bd66265f228`。Actions run 38836767257がsuccess、公開ブラウザ12checks/6operations合格、receipt accepted/adoptionComplete true/exitCode0を確認した。ローカルEdge25・WebKit24と、通常解像度の公開WebKit24もPASS。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=forest-20261016 。森林を生成せず山/道路/JCT/街路樹は保持し、遠い建物は街区モデルへ切替。dataは配信84,612,569bytes／HTTP展開後162,904,246bytes（前便92,787,516／218,766,927）。ブラウザnative gzip、JS展開fallbackなし。実iPhone 17起動はユーザー検証待ち。以下のBrotli対策・ローカル未公開などは各時点の履歴で、今回をiPhone成功と扱わない。

今回の結果は森林なしWeb公開記録を参照。CIの256px software WebGL確認は性能保証ではない。既存classic/gateway・永続data・AirRaceと保持catalog/Bundleをguardで保護し、Unityだけを配備した。
<!-- FOREST_WEB_PUBLICATION_END -->

<!-- IOS_SAFARI_BOOT_START -->
## 現在: iPhone Safariの起動クラッシュに対応（2026-10-15）

ユーザー実機でSafariが繰り返しクラッシュした。PC/WebKit smoke合格をiPhone適合と扱わない。対策版公開済み・iPhone実機の解消は未確認。約93MB→219MBのJS Brotli展開を、ブラウザnative展開へ変更。圧縮byte・展開後byteとUnityゲーム内容は同一。JS/WASMの.br MIMEを補正し、通常Edge/WebKitの確認を行った。実機はiPhone 17、開始ボタンが表示される前にクラッシュすると本人確認済み。原因はメモリ不足の可能性があり、断定していない。

詳細と公開receiptは `docs/head/IOS_SAFARI_BOOT_20261015.md`。以前の公開受入れはPC/ソフトウェアブラウザでの受入れであり、iPhone起動成功の証拠ではない。
<!-- IOS_SAFARI_BOOT_END -->

## 公開採用済み: 2026-10-15 道路網・山地のスマホ用WebGL

Unity source `eeca3f261038b6d6bf271b91157b0a5abf23ac9d`、配布release／Unity RELEASE_TAG `e36ccaf102ee8494aa0d60d4d347f268114a9924`、Unity image `sha256:36e023b1586b3f7db8d0bce9bbecf629821eb78ee62b3341e21f2f69cc69dada`。Actions run [38742023882](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38742023882) がsuccess、2026-10-15 22:27 JSTにreceipt accepted／adoptionComplete true／exitCode0を確認。公開URLの通常解像度Edge25・WebKit24 checksも合格。実iPhone/Android性能は未測定。

公開先: https://unity-games.wos.ktsys.jp/02/colony-racer/ 。高架・南/中央/北環状の移動ボタンを追加。既存Actions認証を使うUnity専用自動配備を追加し、公開ブラウザ後にfinalize、失敗時rollbackまで実動作を確認した。classic/gatewayとruntime dataをguardで保持。詳細は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。以下の公開待ち・未実施は各記録時点の履歴。

## 公開準備中: 2026-10-15 道路網・山地のスマホ用WebGL

Unity `eeca3f261038b6d6bf271b91157b0a5abf23ac9d` から5 IC・3環状線/JCT・盛土中央分離帯・距離案内・DEM山地/森林を含むWebGLを生成。スマホから高架と3環状線へ移動できるボタンを追加。見た目用InfrastructureのCPU meshコピーを除き、森林のみ圧縮、道路Colliderと原Prefabを保持した。Brotli fallbackを使用。AirRace全資産・旧Colony StreamingAssets/TemplateDataをbyte照合して保持。

既存の自動配備はclassic/gatewayのみだったため、既存Actions認証を使うUnity専用workflowを追加。CI・公開受入れ待ちで、公開切替は未実施。記録: `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md`。更新前3文書は `docs/history/20261015-before-colony-road-network/`。

# gamecenter-shinomiya

## 最新成果物: 2026-10-15 Colony Racer既存街並みの外観更新

Unity source `a5c3493a9378480e24a54b99bfe169662fbf028b`から新WebGLを生成。Core/East/Westの外観・道路素材・葉の光を改善し、元の構造・物理とPC／touch操作を保持した。ローカル9描画測定、通常3環境88checks、Native先行7と最終近景1を確認。連続接地は未合格、iPhone実機は未測定。成果物と制限は[今回記録](docs/head/COLONY_STREETSCAPE_20261015.md)。

公開の採用状態は今回rawのpublic-browser-acceptance.jsonとBASE receipt accepted、live Unity image／RELEASE_TAGを照合する。Git mergeやこの文書だけでは公開完了としない。以下の91ef／2026-10-14の『現在』は旧公開の履歴であり、Unity source・配布commit・image・文書commitを区別して再開する。

## 完了（入力・描画prototype公開）: 2026-10-14 Colony Racer共通WebGL

既存Core／East／West、固定躯体・生活街区とP0-P2車体を、[https://unity-games.wos.ktsys.jp/02/colony-racer/](https://unity-games.wos.ktsys.jp/02/colony-racer/) のPC・タッチ共通版へ更新した。PCはW／Space／A・D、スマホは左のアナログ操舵・右の加速と制動。旧公開版にぷにこんがあったという推測は本人確認で訂正し、新しいtouch controllerを採用した。スマホ専用Sites案は中止・未公開。

2026-10-14 23:51 JSTに公開採用を完了した。配布devと永続Unity RELEASE_TAGは `91efbec9032aaa087236e0965d7e0cb16b9ff583`、Unity sourceは `ab3394504e39b7997eeb1e454f82bfb55088ffef`、Unity imageは `sha256:48d91a6cb4d99dc0ff890ad9c63e817e88e59df43ac7c7e05e357933aae4fea6`。accepted receipt／BASE clean checkout／公開PC24checks・touch33checks計528samples／post-final115file hash・gzip・MIME・catalog APIのexit0を照合した。今回の採用は共通controller／render prototypeの公開で、接地安定の受入れとは分ける。

独立 `public-acceptance-audit.json` の7群PASSで同Unity image、対象外132container、runtime6JSON、routing／Compose／gateway設定、AirRace57file、既存Colony StreamingAssets37／TemplateData14を照合した。classic／gatewayはa45dc158のimage／containerを継続し、gatewayはDNS再解決のgraceful reloadだけを行った。runtime dataをGitへ取り込んでいない。

Webの入力・描画smokeと連続接地を区別する。ローカル3環境の88checks／807samplesはsmoke PASS、100km/h以上の近傍路面でcontactが間欠的に外れるため連続接地gateはfalse。motor・操舵はcontactでgateされるのでHUDだけの問題とは扱わない。iPhone hardware・実機fpsは未測定。Native r9の115条件は履歴で、WebGL合格へ転記しない。

結果は [Colony WebGL更新](docs/head/COLONY_WEBGL_20261014.md)、手順は [Unity限定公開](docs/head/COLONY_WEBGL_PUBLICATION.md)。source commit・配布commit・image SHA・実URLを別に照合して再開する。以下は更新前の記録で、旧Unity image041e054と『再ビルド／公開未実施』は各記録時点の履歴。

現在の停止点は共通WebGL prototype公開。連続接地の課題とiPhone実機未測定を残す。作業用Editor・local検証serverは停止済み。文書commitを稼働image SHAと混同せず、accepted receiptとlive状態を先に確認する。

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
