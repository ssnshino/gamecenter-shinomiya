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

## BASE配置

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
