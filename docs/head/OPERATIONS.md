# 配布と運用

このrepoはRustゲームとUnity配布物、公開gatewayを管理する。Unity編集はairraceUnity/colony-racerで行い、出力先を[配置先契約](UNITY_DELIVERY_CONTRACT.md)で指定する。古いrust-sandboxのdeploy workflowを実行しない。

## 検証

```bash
cd apps/unity-web
npm ci
npm run check
cd ../..
node --test tests/game-delivery.test.mjs
SOURCE_SHA=<取り込む配布元の40桁SHA> node scripts/verify-game-delivery.mjs . docs/head/UNITY_ARTIFACT_MANIFEST.json
```

import元のSHA/path/hashはIMPORT_MANIFEST.json、Unityの全配布物・gzip復号hashはUNITY_ARTIFACT_MANIFEST.json。Unity編集元SHAは由来を証明できない限りnullのまま。新Unity成果物に更新する際はmanifestも更新する。

## 初回BASE配置・公開切替（実施済みの履歴）

配置先 `/home/shino/source/repos/upstream/gamecenter-shinomiya`。branch dev。配備は固定SHAを確認し、dirty worktreeなら停止する。各imageタグは実行コードの40桁SHAを指定する。文書のみの追記commitをimage再ビルド理由にしない。

1. 既存container、routing、空きポート、負荷、runtime dataを確認。
2. 新checkoutでrelease SHAを確認し、実行SHAをGit外.env.releaseのRELEASE_TAGに保存。`docker compose --env-file .env.release -f compose.dev.yaml build classic`、unity-web、gatewayの順で1件ずつビルド。
3. 初回は旧dataをruntime/classicに複製して非公開QA。`docker compose --env-file .env.release -f compose.dev.yaml up -d --no-build classic unity-web gateway` はこの新projectだけを対象にする。
4. 127.0.0.1:18094のHTTP、全成果物、catalog、WSを検証。例: `node scripts/smoke-game-delivery.mjs docs/head/UNITY_ARTIFACT_MANIFEST.json http://127.0.0.1:18094/02/ .`。
5. 切替では旧Rustと新classicを停止して書込を止め、旧6JSONの最終backupを作る。runtime/classicへ最終複製、hash一致、所有権を確認してclassicを起動。旧公開Unity containerも停止する。
6. 旧2containerのrouting値からGAMECENTER_PUBLIC_HOSTSを作り、Git外 `.env.routing` に保存。既存proxy設定は編集しない。RELEASE_TAGを保存したGit外 `.env.release` とともに読み、`docker compose --env-file .env.release --env-file .env.routing -f compose.dev.yaml -f compose.public.yaml up -d --no-build --no-deps gateway` でgatewayだけを公開networkに接続。
7. HTTPS、旧URL redirect、root API互換、WS、Unity画面と操作を検証し、実行release SHAと結果をsnapshotへ記録する。

runtime/classicの6JSONは実ユーザーデータ。Git、Docker build context、CI artifactに含めない。検証でランキング投稿を行わない。再配備ではruntimeを上書きしない。新旧classicを同じdataへ同時接続しない。

## Rollback

旧containerと元checkoutを削除しない。公開切替失敗時は新gatewayを停止、classicも停止。新classicのdataを別backupに保存し、構造が同じ6JSONを旧appへ戻す場合はhashを照合してから旧Rustを起動する。旧Unity containerも起動し、旧経路・WSを検証する。新データを無視して古いbackupだけを復元しない。proxy/firewall/volumeを削除しない。

古いrust-sandbox/devは現在Unity入口の配布元であり、1号店の復元元は固定SHA 58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea。unity-rust-games2は別stagingなのでこの手順の対象外。


## classic・共通入口だけの実ビルド／配備

`build-classic-gateway.yml` はdev向けPRと対象コードのbranch更新でclassic/gatewayのDocker imageを実ビルドし、隔離networkでnginx設定を検査する。既存Node検査・成果物テストと、生成manifestが保管manifestに一致することも確認する。README等の文書だけの更新ではこのworkflowを起動しない。既存verify.ymlは維持する。

配備jobはPRを除外し、devかつ `CLASSIC_GATEWAY_DEPLOY_ENABLED=true` の時だけ動く。PR #2をマージしたdevにはliteral falseも残り、同SHAのdeployはskippedだった。解除featureはCIで検証し、設定登録とPR投稿・devマージの本人承認後に有効化する。2026-10-11 03:40 UTC確認時点で新repoのSecrets/Variablesは両方空。設定する値は以下のとおり。

| Actions設定 | 値・登録方法 |
|---|---|
| Secret DEPLOY_DEV_HOST | wos.ktsys.jp |
| Secret DEPLOY_DEV_PORT | 4523 |
| Secret DEPLOY_DEV_SSH_KEY | 本人が既存dev用鍵を安全なGitHub入力画面で登録。agentは内容を取得・表示・転記しない |
| Variable DEV_DEPLOY_REPO_PATH | /home/shino/source/repos/upstream/gamecenter-shinomiya |
| Variable DEV_DEPLOY_KNOWN_HOSTS | 照合済みの[wos.ktsys.jp]:4523 ed25519公開鍵。fingerprint SHA256:jxrQwD92EJgL/MQZ41cEGG54w+RsgW3FuBHelFoP0Cc |
| Variable CLASSIC_GATEWAY_DEPLOY_ENABLED | 本人承認後にtrue。未設定/falseなら配備しない |

ホスト鍵は引き継ぎ値、既存known_hosts、信頼済みBASE接続、現在の公開接続先で一致を確認した。再開時は再照合し、不一致なら停止する。旧repoのSecretは読み出せる前提にせず、共通DEPLOY_SSH_KEYを使わない。新しい鍵やrunnerを作成しない。Secret名の存在確認だけでSSH接続成功とは扱わない。

CIでビルド検証後、既存SSH経路でBASEに接続し、固定SHAのソースからclassic/gatewayを順次ビルドする。registryやimage転送方式は追加しない。clean dev、origin、最新dev SHA、fast-forward、サーバlock、公開Compose、runtime6JSONの存在/JSON妥当性/所有者と、稼働classicの/dataが同じRW bindであることを確認する。Unityコードや保管manifestの差分がある時はこの経路で配備しない。

個別タグ `CLASSIC_RELEASE_TAG` / `GATEWAY_RELEASE_TAG` は未指定なら従来 `RELEASE_TAG` を使う。配備ではこの2つだけを更新し、既存 `RELEASE_TAG` とunity-web imageを保つ。`compose.dev.yaml` と `compose.public.yaml` を併用して `up -d --no-build --no-deps --force-recreate classic`、続いて `gateway` を実行する。gateway再作成でclassicの名前解決も更新する。既存unity-webのcontainer ID・image・startedAt・restart回数を前後比較する。

短い1号店停止とWebSocket切断の可能性がある。runtime/classicは上書き・初期化しない。公開後に共通入口・Rust API/WS・redirect・Unity配布物hash/APIを確認する。実ブラウザ操作は別確認。公開smokeに失敗しても自動で旧データを復元しない。

失敗時は処理を止め、runtime/deploy/classic-gateway-*.jsonの旧image/checkout SHAと切替段階、ログを確認する。receiptのlocal-verified-public-pendingは公開確認完了ではなく、公開確認の結果は同じActions runで確認する。必要な復旧は以前の個別タグへ戻してclassic/gatewayだけを上記--no-deps方式で再作成し、runtimeとUnityは保持する。実行前にlive dataと状態を確認し、別途承認を得る。途中失敗時は実containerと.env.release記録が異なる場合があるため、ファイルだけで稼働版を判断しない。旧全体RELEASE_TAGへ戻すために全serviceを再作成しない。

PR #2後のdev 25c625e3ba441655c33cf3e868cfca086cbd2088では、[Docker build CI run 38105519621](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519621)と[verify run 38105519655](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38105519655)がsuccess。classic/gatewayのDocker build、隔離DNSのnginx設定検査、Node/Rust検証、保管manifest比較、Python guardテストは実行済み。新経路のBASE配備とその配備後公開確認は未実施。初回公開の稼働release 041e0548362a2040bfd94d518866a04456849e05を、CI build済みSHAと区別する。

有効化手順は、featureの変更・CI結果・投稿先とPR本文全文・公開への影響を提示して本人承認をまとめて得る → 接続設定を登録し本人がSSH鍵Secretを入力 → 設定とdev/BASE状態を再確認 → 有効化PRをdevへマージ → 同pushの1回の自動配備を確認 → 前後比較、公開HTTP/WS/114配布ファイルhashと実ブラウザを検証、の順。手動dispatchや同じ配備の重複実行をしない。失敗時は同runと実状態を調べてから再実行範囲を判断する。

配備前にUnityのcontainer ID/image ID/tag/StartedAt/restarts、114ファイルのinventory hash、runtime6JSONの個別hash/サイズ/JSON妥当性/所有者を記録する。配備後は同じ基準で比較する。公開利用によるJSON更新があれば差分の整合性を確認し、hash不一致を黙って保持成功としない。検証でスコアを投稿しない。秘密値・data本文を文書やCI artifactに含めない。
