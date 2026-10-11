# 現在地: 2026-10-11 JST — classic/gateway自動配備・公開検証済み

統合公開後、本人の「既存の鍵を使う従来方式で完遂」の指示に従い、自動配備を有効化してdevマージによる1回のclassic/gateway配備と公開検証を完了した。Unity編集ソースは各repoに残し、既存配布物・image/container・データを保持した。

## 現在の公開と配備

- 共通入口: https://unity-games.wos.ktsys.jp/
- 1号店: https://unity-games.wos.ktsys.jp/01/
- 2号店: https://unity-games.wos.ktsys.jp/02/
- 配布repo: ssnshino/gamecenter-shinomiya、default/運用branch dev。
- Mac: /Volumes/SSD250GBUSB/source/repos/upstream/gamecenter-shinomiya。
- BASE: /home/shino/source/repos/upstream/gamecenter-shinomiya。
- classic/gateway実行release SHA: a45dc158dbe1785d971e597ec16d95fe9e77bd4e（PR #3のdevマージ）。
- Unity実行release SHA: 041e0548362a2040bfd94d518866a04456849e05。後続の配備script修正・文書commitをimageの実行SHAと混同しない。
- Compose project gamecenter-shinomiya。container/serviceはgamecenter-shinomiya-classic / classic、gamecenter-shinomiya-unity-web / unity-web、gamecenter-shinomiya-gateway / gateway。
- classicとunity-webは内部3000、gatewayの確認ポートは127.0.0.1:18094 → 80。公開gatewayだけを既存wos-proxy-networkへ接続。既存proxy設定ファイル、鍵/firewall/NAT/runnerは変更していない。
- 初回公開切替は2026-10-11 01:12:08 JSTに完了。その後のclassic/gateway自動更新は13:07 JST。3container running/restarts=0。

## 2026-10-11 — 1回の自動配備と保全確認

- [PR #3](https://github.com/ssnshino/gamecenter-shinomiya/pull/3)を04:04:57 UTCにdevへマージ。PRの[Docker CI 38110287938](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110287938)と[verify 38110288061](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110288061)は事前に成功した。
- dev a45dc158dbe1785d971e597ec16d95fe9e77bd4eの[build/deploy 38110443542](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443542)と[verify 38110443571](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443571)はsuccess。既存dev用SecretでSSH接続し、classic→gatewayだけを--no-depsで更新。手動dispatch・再実行は0回。

| service | 実行image tagのSHA | BASEで照合したimage ID |
|---|---|---|
| classic | a45dc158dbe1785d971e597ec16d95fe9e77bd4e | sha256:3f4a29feae5aedf74b2a2d64506618148ee2636efa9338a6753da4f40611608f |
| gateway | a45dc158dbe1785d971e597ec16d95fe9e77bd4e | sha256:23cd0831ae7295e4841839a96ae39b1b78dcf4de9e72485780b505681482b1a5 |
| unity-web | 041e0548362a2040bfd94d518866a04456849e05 | sha256:5aaf891d0e7c167a87e6bfe633f044c15538d2e1483419306542c8616740afbf |

- 各tagが指すimage IDと稼働containerのImageが一致。classicのGIT_HASHはa45dc158dbe1785d971e597ec16d95fe9e77bd4e。classic StartedAt=04:07:22 UTC、gateway=04:07:25 UTC。Unityはcontainer ID 4bc818141ac1623ef74dacb6f45ae3fcbf6aa7a92cffa2a22a94d74985253dbe、StartedAt=2026-10-10 16:09:03 UTC、image/restarts=0を含め前後一致。
- 同じActions runでUnity全114ファイルのHTTP hash・gzip復号・MIME/catalog APIとportal/classic API/WSを検証。追加確認ではHTTP15経路、classic/portal静的24ファイルhash、query保持redirect6件、互換Bundle2件とroot catalog API6比較、classic WS7経路のJSON状態受信が成功。
- Macの実ブラウザでportal/両店menu、Pongの描画と上入力、AirRace ROUND1の開始・飛行・旋回、Colony ROUND2の開始・歩行・旋回を確認。観察したconsole errorは0。スコア・ゴーストを投稿していない。
- Unity114ファイルとmanifestのhash inventoryは配備前と一致。runtime/classicの6JSONは個別hash・サイズ・JSON構造・uid/gid=1000・mode=0644が一致、合計7,177,421 bytesを保持。Unityを含む対象外131コンテナのID/image/state/StartedAt/restartsも前後一致。routingファイルは無変更。Unity再ビルド、旧workflow/旧container再実行、Godot・runner・firewall変更は行っていない。
- 配備後照合で.env.releaseの個別タグ未保存を発見。SSHのbash -sの残りの標準入力をcompose execが読み取ったため、runのBASE stepがnginx -t後に終了していた。公開検証stepは成功。04:12 UTCにlock/clean/稼働SHA/保全guardを再確認し、nginx -t・local health2経路・タグ記録だけを補完した。再build・再作成は行っていない。RELEASE_TAGは旧Unity SHAのまま、CLASSIC_RELEASE_TAG/GATEWAY_RELEASE_TAGはa45dc158dbe1785d971e597ec16d95fe9e77bd4eに保存済み。
- [PR #4](https://github.com/ssnshino/gamecenter-shinomiya/pull/4)の修正はnginx -tへのstdinを/dev/nullにする1行と回帰テスト。修正前の早期終了を再現し、修正後はhealth・保全検証・タグ保存まで到達。ブランチ[Docker CI 38110872759](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110872759)と[verify 38110872746](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110872746)、PRの[Docker CI 38110956338](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110956338)と[verify 38110956411](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110956411)はsuccess。04:18:05 UTCにdevへマージした修正SHAはce2a22b9f25e60f9cd7e250f7afa35ba693d803d。
- PR #4のマージ時だけ配備変数をfalseにし、同SHAの[Docker CI 38111146311](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146311)と[verify 38111146286](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146286)のsuccess・deploy skippedを確認してtrueへ戻した。CIでbuildした修正SHAと、稼働classic/gatewayのa45dc158dbe1785d971e597ec16d95fe9e77bd4eは区別する。アプリ・gateway・Compose・Unityのソース差分はなく、2回目のBASE配備は行っていない。
- 自動配備receiptはruntime/deploy/classic-gateway-a45dc158dbe1785d971e597ec16d95fe9e77bd4e-20261011T040657Z.json。元のphase=local-verification/status=local-verified-public-pending/exitCode=0を保全し、それだけでタグ保存・公開完了と扱わない。公開結果は上記Actions run、補完・前後比較はMacの/tmp/gamecenter-shinomiya-classic-gateway-20261011/に記録。秘密値・data本文は含めていない。

## classic/gateway有効化前の確認（2026-10-11 03:40 UTC / 12:40 JST）

- PR #2は2026-10-11 02:33 UTCにdevへマージ済み。当時のdev SHAは25c625e3ba441655c33cf3e868cfca086cbd2088。
- 同SHAの[Docker build CI run 38105519621](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519621)と[配布検証run 38105519655](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519655)はsuccess。classic/gatewayの実ビルド、nginx設定、Node/Rust検証、成果物manifest照合、guardテストを実施済み。deploy jobはliteral falseによってskipped。
- BASEのcheckoutはclean dev、HEAD d39f535d4248625f9e937247a100e51f1e0944ce。稼働classic/gateway/unity-webのimage tagとclassic GIT_HASHは全て041e0548362a2040bfd94d518866a04456849e05。3container running、restarts=0。CIでビルド済みのSHAを稼働済みとは扱わない。
- この確認時点では新repoのActions SecretsとVariablesは両方空で、設定登録・有効化PRの投稿・devマージは承認待ちだった。後述の本人の継続指示により従来方式で登録した。共通DEPLOY_SSH_KEYや新規鍵を使用しない。
- DEV_DEPLOY_KNOWN_HOSTSのed25519 fingerprintはSHA256:jxrQwD92EJgL/MQZ41cEGG54w+RsgW3FuBHelFoP0Cc。引き継ぎ公開鍵、Macの既存known_hosts、StrictHostKeyChecking=yesの既存BASE接続で得たホスト公開鍵、wos.ktsys.jp:4523の現在の取得値が一致。
- 配備前基準: Unity container/image/StartedAt/restarts、既存114ファイルのhash inventory、runtime/classicの6JSONのhash/サイズ/JSON妥当性/uid=1000を確認。6JSONは合計7,177,421 bytes。data本文や秘密値は記録に含めていない。
- 有効化用の変更はworkflowのliteral false解除と事実記録のみ。配備変数、dev限定/PR除外、strict known_hosts、最新SHA/clean fast-forward、flock、個別タグ、classic→gatewayの--no-deps更新は維持する。
- 新経路のBASE build/deployと配備後のHTTP/WS/公開114ファイル/実ブラウザ/データ保持検証は未実行。Unity再ビルド、他アプリ・Godot・runner・firewallの変更は対象外。

## 2026-10-11 03:59 UTC / 12:59 JST — 設定登録済み・自動配備前

- 本人から既存鍵を使う従来方式で完遂する指示を受け、設定登録・PR投稿・devマージと1回の自動配備を継続する。手入力ハンドオフを必須とした先の手順を更新した。
- 旧rust-sandboxの[PR #68](https://github.com/ssnshino/rust-sandbox/pull/68)と成功run 38057134781を読み取り確認し、既存ssh base用鍵がdev専用Secretの先例だと同定。ssh-agentなし・その鍵のみ・strict known_hostsでwos.ktsys.jp:4523への認証成功。旧workflowや旧containerは実行していない。
- 新repoにDEPLOY_DEV_HOST/DEPLOY_DEV_PORT/DEPLOY_DEV_SSH_KEYのSecretと、DEV_DEPLOY_REPO_PATH/DEV_DEPLOY_KNOWN_HOSTS/CLASSIC_GATEWAY_DEPLOY_ENABLED=trueのVariableを登録しmetadataを確認。秘密鍵はCLIの標準入力からGitHubへ暗号化登録し、本文をチャット・ログ・添付へ出力していない。既存鍵の権限・BASE authorized_keysは変更していない。
- workflow変更commit 09c0385f52467451ef1ac61c0182c0cfe996a51aのDocker CI run 38109240822とverify run 38109240828はsuccess、featureのdeployはskipped。BASEの実効Compose/runtime guard、公開HTTP/API/7本のWS、Unity全114ファイルとclassic静的24ファイルのhash、redirect6件、Unity互換Bundle2件とroot catalog APIを配備前に確認済み。
- この時点では有効化PRのdevマージ・新経路のBASE配備・配備後検証は未実行。稼働3imageは引き続き041e0548362a2040bfd94d518866a04456849e05。

## 初回公開切替の確認結果（履歴）

- ローカル型検査、15件の成果物テスト、GitHub CI success（run 38066409344）。RustはBASEで1 compilation jobのrelease build。Node/gatewayのbuildも順次完了。nginx -t success。
- 非公開HTTP: 共通入口、1号店の全ゲームpage/API/代表module/image、2号店の入口/health/catalog HTTP200。/01・/02・ゲームpathの末尾slash補完は308、query保持。
- 公開HTTPS/TLS検証成功。1号店入口/Pong/status HTTP200。1号店7本のWSは全てHTTP101・accept妥当・JSON状態受信（fighting/2pは既存Start protocolを送ってwaiting状態受信）。
- Unity2ゲームは各57ファイル、合計114ファイルを公開HTTPで全hash検証。gzip復号hash、WASM/JS MIME、catalog APIと既存root APIを照合。
- 既存compiled resolverの /02/StreamingAssets/* はRefererでゲームを限定する互換経路を追加。AirRace/Colonyの同名Bundleが各ゲームのhashと一致、private/no-store・Vary: Refererを確認。Referer不明の曖昧なURLは404。
- 公開ブラウザ: 共通入口と両店のmenu、PongのWS描画・上下入力、AirRace ROUND1の開始・飛行・旋回、Colony ROUND2の開始・歩行で状態変化を確認。観察したコンソールerrorは0。既存UnityのpersistentDataPath非推奨warningは残る。
- 旧rust-sandbox URLは新/01へ308。旧/airrace3d/・/colony-racer/は新/02配下へ308。旧Rust root WS/APIは既に開いていたpage用に互換維持。

## 初回公開切替のデータとrollback（履歴）

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
