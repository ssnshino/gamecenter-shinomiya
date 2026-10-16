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

## 2026-10-15 Unity自動配備の追加（検証・公開待ち）

今回のスマホ向けデプロイ依頼と自動配備の確認を受け、Unity専用 `.github/workflows/deploy-unity-web.yml` を追加。dev更新で既存Actions認証を利用し、Unity限定仮配備、実公開ブラウザでの起動・運転確認、finalizeの順に進め、受入れ失敗時はrollbackする。classic/gateway workflow、鍵、runner、firewallは変更しない。以下の旧作業範囲は記録当時のもの。現在の証拠は `docs/head/COLONY_ROAD_NETWORK_WEB_20261015.md` に記録し、accepted receipt確認まで公開完了と扱わない。

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

配備jobはPRを除外し、devかつ `CLASSIC_GATEWAY_DEPLOY_ENABLED=true` の時だけ動く。PR #2時点のliteral falseはPR #3で解除済み。本人の従来方式で完遂する指示に従い、2026-10-11 03:59 UTCに以下を登録し、devマージのbuild/deploy run 38110443542で既存dev用鍵によるSSHとclassic/gateway更新・公開検証の成功を確認した。設定登録前のSecrets/Variables空状態と、CI build済みだが未配備だった時点はsnapshotの履歴を参照。

| Actions設定 | 値・登録方法 |
|---|---|
| Secret DEPLOY_DEV_HOST | wos.ktsys.jp |
| Secret DEPLOY_DEV_PORT | 4523 |
| Secret DEPLOY_DEV_SSH_KEY | PR #68と同じ既存ssh base用鍵。本人の承認範囲でCLI標準入力からGitHubへ暗号化登録し、本文をチャット・ログ・添付へ出力しない |
| Variable DEV_DEPLOY_REPO_PATH | /home/shino/source/repos/upstream/gamecenter-shinomiya |
| Variable DEV_DEPLOY_KNOWN_HOSTS | 照合済みの[wos.ktsys.jp]:4523 ed25519公開鍵。fingerprint SHA256:jxrQwD92EJgL/MQZ41cEGG54w+RsgW3FuBHelFoP0Cc |
| Variable CLASSIC_GATEWAY_DEPLOY_ENABLED | trueでdevの対象変更を自動配備。未設定/falseなら配備しない。修正だけを配備せず反映する時は一時falseにし、対象runのdeploy skipped確認後に戻す |

ホスト鍵は引き継ぎ値、既存known_hosts、信頼済みBASE接続、現在の公開接続先で一致を確認した。再開時は再照合し、不一致なら停止する。旧repoのSecretは読み出せる前提にせず、共通DEPLOY_SSH_KEYを使わない。新しい鍵やrunnerを作成しない。既存dev鍵の同定は旧PR #68と成功run 38057134781の読み取り記録を使い、ssh-agentなしで公開接続先への認証を確認した。Secret名の存在確認だけでActionsからのSSH接続成功とは扱わず、配備runで実接続を確認する。

CIでビルド検証後、既存SSH経路でBASEに接続し、固定SHAのソースからclassic/gatewayを順次ビルドする。registryやimage転送方式は追加しない。clean dev、origin、最新dev SHA、fast-forward、サーバlock、公開Compose、runtime6JSONの存在/JSON妥当性/所有者と、稼働classicの/dataが同じRW bindであることを確認する。Unityコードや保管manifestの差分がある時はこの経路で配備しない。

個別タグ `CLASSIC_RELEASE_TAG` / `GATEWAY_RELEASE_TAG` は未指定なら従来 `RELEASE_TAG` を使う。配備ではこの2つだけを更新し、既存 `RELEASE_TAG` とunity-web imageを保つ。`compose.dev.yaml` と `compose.public.yaml` を併用して `up -d --no-build --no-deps --force-recreate classic`、続いて `gateway` を実行する。gateway再作成でclassicの名前解決も更新する。既存unity-webのcontainer ID・image・startedAt・restart回数を前後比較する。health・保全確認後に2つの個別タグを.env.releaseへ保存する。

SSHの `bash -s` はスクリプト自体を標準入力で読むため、`compose exec -T gateway nginx -t </dev/null` としてexecへ残りのスクリプトを渡さない。`-T`だけではstdin消費を防げず、後続検証・タグ保存前に成功終了することがある。PR #4の回帰テストはこの早期終了を再現し、health2経路・Unity保全・RELEASE_TAGと既存設定の保持・個別タグ保存まで到達することを検証する。

短い1号店停止とWebSocket切断の可能性がある。runtime/classicは上書き・初期化しない。公開後に共通入口・Rust API/WS・redirect・Unity配布物hash/APIを確認する。実ブラウザ操作は別確認。公開smokeに失敗しても自動で旧データを復元しない。

失敗時は処理を止め、runtime/deploy/classic-gateway-*.jsonの旧image/checkout SHAと切替段階、ログを確認する。receiptのlocal-verified-public-pendingは公開確認完了ではなく、公開確認の結果は同じActions runで確認する。必要な復旧は以前の個別タグへ戻してclassic/gatewayだけを上記--no-deps方式で再作成し、runtimeとUnityは保持する。実行前にlive dataと状態を確認し、別途承認を得る。途中失敗時は実containerと.env.release記録が異なる場合があるため、ファイルだけで稼働版を判断しない。旧全体RELEASE_TAGへ戻すために全serviceを再作成しない。

今回の実行: [PR #3](https://github.com/ssnshino/gamecenter-shinomiya/pull/3)のdevマージSHA a45dc158dbe1785d971e597ec16d95fe9e77bd4eを[build/deploy run 38110443542](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443542)で1回配備。[verify run 38110443571](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38110443571)もsuccess。両serviceの同SHAのtag/image IDとclassicのGIT_HASHを照合し、Unityの041e0548362a2040bfd94d518866a04456849e05を保持した。公開114ファイルhash/API/WS、Macブラウザの基本操作、Unity・runtime6JSON・対象外コンテナ・routingの前後一致を確認した。

同runのBASE stepはnginx -t後にstdinを消費して終了していたため、配備後の照合で.env.releaseの個別タグ未保存を発見した。04:12 UTCに稼働SHA・clean/lock・保全基準を確認し、nginx -t/local health/個別タグ保存だけを補完。再build・container再作成・run再実行は行っていない。元receiptのphase=local-verificationとexitCode=0だけでは後続処理の完了を証明しない。公開結果はActions run、補完とimage/data保持結果はsnapshotへ記録した。

今回の有効化は、本人の完遂指示に従い既存dev鍵をCLI標準入力で暗号化登録 → 設定とdev/BASE・ホスト鍵/保全基準を再確認 → PR #3のCI成功後にdevマージ → 同pushの1回の自動配備と公開検証 → 実状態の前後比較とブラウザ検証、の順に実施した。手入力ハンドオフは不要とされた。手動dispatchや同じ配備の重複実行をしない。失敗時は同runと実状態を調べてから再実行範囲を判断する。

PR #4の配備script修正は04:18 UTCに配備変数を一時falseにしてdev反映済み。修正SHA ce2a22b9f25e60f9cd7e250f7afa35ba693d803dの[Docker CI 38111146311](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146311)と[verify 38111146286](https://github.com/ssnshino/gamecenter-shinomiya/actions/runs/38111146286)がsuccess、deployはskipped。その確認後に変数をtrueへ戻した。BASEの稼働releaseはa45dc158dbe1785d971e597ec16d95fe9e77bd4eを保持し、修正CIのbuild済みSHA・文書のみのcommitと区別する。

配備前にUnityのcontainer ID/image ID/tag/StartedAt/restarts、114ファイルのinventory hash、runtime6JSONの個別hash/サイズ/JSON妥当性/所有者を記録する。配備後は同じ基準で比較する。公開利用によるJSON更新があれば差分の整合性を確認し、hash不一致を黙って保持成功としない。検証でスコアを投稿しない。秘密値・data本文を文書やCI artifactに含めない。
