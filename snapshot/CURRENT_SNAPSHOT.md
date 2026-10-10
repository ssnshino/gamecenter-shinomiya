# 現在地: 2026-10-11 JST — 統合公開済み

ユーザーの「１号店、２号店公開まですすめて！」に従い、統合実装、GitHub作成/反映、BASE配備と公開切替を完了した。Unity編集ソースは各repoに残した。

## 現在の公開と配備

- 共通入口: https://unity-games.wos.ktsys.jp/
- 1号店: https://unity-games.wos.ktsys.jp/01/
- 2号店: https://unity-games.wos.ktsys.jp/02/
- 配布repo: ssnshino/gamecenter-shinomiya、default/運用branch dev。
- Mac: /Volumes/SSD250GBUSB/source/repos/upstream/gamecenter-shinomiya。
- BASE: /home/shino/source/repos/upstream/gamecenter-shinomiya。
- 実行release SHA: 041e0548362a2040bfd94d518866a04456849e05。以後の記録用commitは文書のみで、imageの実行SHAと区別する。
- Compose project gamecenter-shinomiya。container/serviceはgamecenter-shinomiya-classic / classic、gamecenter-shinomiya-unity-web / unity-web、gamecenter-shinomiya-gateway / gateway。
- classicとunity-webは内部3000、gatewayの確認ポートは127.0.0.1:18094 → 80。公開gatewayだけを既存wos-proxy-networkへ接続。既存proxy設定ファイル、鍵/firewall/NAT/runnerは変更していない。
- 切替完了 2026-10-11 01:12:08 JST。3container running/restarts=0、他の既存containerのrunning/startedAt変化は0件。

## 確認結果

- ローカル型検査、15件の成果物テスト、GitHub CI success（run 38066409344）。RustはBASEで1 compilation jobのrelease build。Node/gatewayのbuildも順次完了。nginx -t success。
- 非公開HTTP: 共通入口、1号店の全ゲームpage/API/代表module/image、2号店の入口/health/catalog HTTP200。/01・/02・ゲームpathの末尾slash補完は308、query保持。
- 公開HTTPS/TLS検証成功。1号店入口/Pong/status HTTP200。1号店7本のWSは全てHTTP101・accept妥当・JSON状態受信（fighting/2pは既存Start protocolを送ってwaiting状態受信）。
- Unity2ゲームは各57ファイル、合計114ファイルを公開HTTPで全hash検証。gzip復号hash、WASM/JS MIME、catalog APIと既存root APIを照合。
- 既存compiled resolverの /02/StreamingAssets/* はRefererでゲームを限定する互換経路を追加。AirRace/Colonyの同名Bundleが各ゲームのhashと一致、private/no-store・Vary: Refererを確認。Referer不明の曖昧なURLは404。
- 公開ブラウザ: 共通入口と両店のmenu、PongのWS描画・上下入力、AirRace ROUND1の開始・飛行・旋回、Colony ROUND2の開始・歩行で状態変化を確認。観察したコンソールerrorは0。既存UnityのpersistentDataPath非推奨warningは残る。
- 旧rust-sandbox URLは新/01へ308。旧/airrace3d/・/colony-racer/は新/02配下へ308。旧Rust root WS/APIは既に開いていたpage用に互換維持。

## データとrollback

6JSON（scores 5種類とairrace_ghosts）の合計7,177,421 bytesを、旧Rust停止後に最終backup・複製し、全ファイルのcmp一致とJSON妥当性を確認。

- BASE backup: runtime/backups/20261011-011137-precutover。
- live data: runtime/classic。Gitとimage build contextから除外。
- 詳細hash/操作前container状態/切替receiptはBASEのruntime/deployへ保存。秘密値やユーザーdata本文はこの文書へ転記していない。
- 旧ayano-lab-rust-sandboxとayano-lab-unity-rust-games-webは停止して保全、restart policyは両方no。元repo/data/image/volumeを削除していない。
- rollbackはdocs/head/OPERATIONS.md。新dataへの書込後は新dataも退避・整合してから戻し、古いbackupだけで上書きしない。

## Unity source repoの配置先文書

- airraceUnity/dev: PR16 merged。mainは異なるUnityコードなので、PR17でREADMEと配置先文書だけを追加。
- colony-racer/dev: PR2 merged。
- 編集元workspaceのHEAD/branch/dirtyは変更せず、別worktreeで文書だけを反映。builder既定値・Unityコード・設定は変更せず、次回buildで新出力先overrideが必要。

## 取り込み元と旧状態

- 1号店: ssnshino/rust-sandbox、旧BASE /home/shino/source/repos/upstream/rust-sandbox、dev 58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea、旧service/project rust-sandbox、18081 → 3000。
- 2号店: 同repoの旧BASE /home/shino/source/repos/upstream/unity-rust-games、dev 7b77aab5c3a3d325ce5ef4a27ade33a3d10669d8、旧service airrace-web/project unity-rust-games、18093 → 3000。
- unity-rust-games2/main a334324fc1cc775b44a662457b53ae9b09fc7b7cは別AIRRACE3D2 staging。今回使用・変更していない。
- Unity compiled成果物は無変更。source Unity SHAの由来は未確定なので、最新Unity sourceから再ビルドしたとは報告しない。IMPORT_MANIFESTとUNITY_ARTIFACT_MANIFESTを参照。

## 既存の未実装と未確認

観察した /api/airrace3d/aircraft-models と /api/colony-racer/aircraft-models は404。取り込み元Node serverのrouteにも実装がなく、Unityは機体データのfallbackを使う。今回の移行でゲーム仕様を補完していない。起動・基本操作の確認と、全ゲーム機能が正常という主張を区別する。

全ラウンド完走、実機スマートフォン、スコア投稿・長時間対戦、host再起動後のacceptanceは未確認。新コンテナはrestart unless-stopped。共通portalはdesktopで確認。新Unity builder pathでの再ビルドは未実施。
