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

## classic/gateway有効化前の確認（2026-10-11 03:40 UTC / 12:40 JST）

- PR #2は2026-10-11 02:33 UTCにdevへマージ済み。最新dev SHAは25c625e3ba441655c33cf3e868cfca086cbd2088。
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
