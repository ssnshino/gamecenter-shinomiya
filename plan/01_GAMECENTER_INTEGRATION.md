# 1号店・2号店の配布統合計画

2026-10-11 JST: 統合公開切替と検証を完了。続いてPR #3をdevへマージし、既存dev鍵でclassic/gatewayを1回自動配備。run 38110443542とverify 38110443571はsuccess、公開HTTP/WS/hash・Macブラウザ・データ保全を確認した。稼働classic/gatewayはa45dc158dbe1785d971e597ec16d95fe9e77bd4e、Unityは041e0548362a2040bfd94d518866a04456849e05。現在の構成と証拠はsnapshot/CURRENT_SNAPSHOT.mdを参照。以下は移行計画の原記録。Unityソースや既存ゲームの仕様変更、旧配置の削除は行っていない。

作成時の記録（2026-10-11 JST）: 方針合意、設計・配置先文書を作成。この時点では実装・公開切替は未実施。現在は上記のとおり統合公開済み。

## 目的と範囲

公開入口と配布repoを `ssnshino/gamecenter-shinomiya` に揃える。`rust-sandbox/main`、旧dev、新dev、ローカルunity-rust-games、別staging unity-rust-games2の混同をなくす。

対象は1号店のRust/axumゲーム、現行2号店のNode/Fastifyサーバー、AirRace3DとColony Racerの既存WebGL/AssetBundle/JSON、および公開入口。Unityの編集ソースはそれぞれssnshino/airraceUnityとssnshino/colony-racerに残す。AIRRACE3D2の再構築stagingは取り込まない。

初回移行でUnityの再ビルド、ゲーム仕様変更、鍵/runner/firewall/NATの変更、元repoの削除、旧workflowの再実行、永続データの初期化をしない。

## 取り込み元を固定する

| 対象 | repo / SHA | 用途 |
|---|---|---|
| 1号店 | ssnshino/rust-sandbox / 58e6f73cfd2bf78e7d7612fc0b0f75ab909d5bea | BASEで同定した稼働Rustソース |
| 2号店 | ssnshino/rust-sandbox / 7b77aab5c3a3d325ce5ef4a27ade33a3d10669d8 | 現行Node配信と配布物 |
| AirRace編集元 | ssnshino/airraceUnity / ea35918fe58d30694cd74f3b78c1a33b46580b77 | Unityソースと配置先文書 |
| Colony編集元 | ssnshino/colony-racer / 0c015ab6550034d02c2790570885753423b16795 | Unityソースと配置先文書 |

取り込み時にlive branch/HEAD/dirtyを再確認する。UnityソースHEADを既存WebGLのビルド元SHAと断定しない。旧repoの履歴は残し、固定SHA・元path・移行先path・raw SHA256を取り込みmanifestへ記録する。現在のunity-rust-games作業場には未commit変更があるため、取り込みは固定Git objectから行い、dirtyなファイルを混ぜない。

## 新repoの配置案

```text
gamecenter-shinomiya/
  apps/
    classic/                 # 旧1号店 app/ のRustソース
    unity-web/               # 現行 web/ のNode/Fastifyサーバー
      public/
        airrace3d/           # WebGL / StreamingAssets / TemplateData
        colony-racer/
  gateway/                   # 共通入口と /01/ /02/ の振り分け
  scripts/                   # 取り込み・配布物検証・smoke
  docs/head/
  plan/
  snapshot/
  compose.dev.yaml
```

これは予定構成で、ゲームコードはまだ配置していない。GitHub repo名、Mac配置、BASE配置は同じgamecenter-shinomiyaへ揃える。devとmainは同じ構成を共有し、branchによって店が変わる状態を作らない。1repo内のComposeでgateway、classic、unity-webを管理し、RustとNodeの実行環境を保つ。

## 公開URLと振り分け

| URL | 移行後の用途 |
|---|---|
| / | 共通ゲームセンター入口 |
| /01 と /02 | 末尾slash付きへ308 redirect |
| /01/ | 1号店のゲーム選択 |
| /01/pong、/01/breakout 等 | Rustゲーム |
| /01/ws、/01/ws2p、/01/ws/* | 1号店WebSocket |
| /01/api/* | 1号店API |
| /02/ | Unityゲーム選択 |
| /02/airrace3d/ | AirRace3D |
| /02/colony-racer/ | Colony Racer |
| /02/api/airrace3d/*、/02/api/colony-racer/* | 2号店API |

gatewayは店のprefixを取り除いて各内部サーバーへ転送する。WebSocket Upgrade、接続継続、query string、正しいMIMEとgzip配信を保つ。内部サービスの公開ポートや既存proxy接続方法は配備前に同定し、ここでは空きポートを推測して決めない。

### 1号店で必要な修正

現在のHTML/JSには `/pong`、`/favicon.ico`、`/api/status`、`/ws` などドメイン直下の参照がある。クライアントへbase pathを渡し、メニュー、CSS/JS、favicon、manifest、API、全WebSocketの生成を `/01` 配下に揃える。HTML本文を書き換えるproxyのsub_filterだけに依存しない。manifestのstart_url/scopeやTruckers・Canvas AirRaceのモジュール参照も確認する。

### 2号店と既存WebGLの互換性

Nodeのホーム画面のゲームリンクを `/02/airrace3d/` と `/02/colony-racer/` に変える。Unity生成HTMLのBuild・TemplateData・StreamingAssetsは相対参照なので、末尾slash付きのゲームURLとその配下の静的ファイル転送を保つ。

現行UnityクライアントはApplication.absoluteURLのscheme/authorityと `/api/airrace3d/*` または `/api/colony-racer/*` を結合する。既存WebGLをそのまま移行するため、gatewayにこの2種類のドメイン直下APIだけの互換経路を残し、unity-webへ転送する。APIを新prefixだけに変更して既存クライアントを壊さない。汎用 `/api/*` を無条件にUnityへ渡さない。

旧Unity URLの `/airrace3d/` と `/colony-racer/` は新URLへredirectする案。ゲーム子path、query、gzip/MIME、cache挙動を検証する。旧1号店domainの廃止・redirectはWebSocketクライアントの扱いも含め別の切替手順にする。

## 配布物と永続データ

初回は現行配布物を固定SHAから取り込み、全ファイルのサイズ・raw SHA256・gzip復号後SHA256、HTMLのloader参照、catalog/Bundle参照を検証する。Unityソースの由来が確認できない成果物はsource SHA unknownとして保持し、新ビルド済みと報告しない。

Rustコードはbreakout_scores.json、dungeon_scores.json、fighting_scores.json、truckers_scores.json、airrace_scores.json、airrace_ghosts.jsonを実行時の相対pathで読み書きする。実ファイルの存在と実マウントを配備前に確認し、対象のバックアップ・保全方法を決める。実ユーザーデータをGitへ取り込まず、旧コンテナと新コンテナから同じJSONへ同時書込みさせない。volume削除や初期化を移行方法にしない。

## Unity repoに残す配置先情報

両repoのREADME、docs/head、snapshotに新repo・公開URL・Mac出力先・BASE予定配置を記載する。builderは既存の出力先上書きを使える。

- AirRace: AIRRACE_WEBGL_BUILD_PATH と AIRRACE_STREAMING_SYNC_ROOT。
- Colony: COLONY_RACER_WEBGL_BUILD_PATH と COLONY_RACER_STREAMING_SYNC_ROOT。

予定pathはdocs/head/UNITY_DELIVERY_CONTRACT.mdで管理する。旧既定path・release script・EditorのAPI base URLが移行済みとは扱わない。Unity設定やソースの変更・ビルドは文書更新とは別に検証する。

## 実装・検証・切替の順序

1. 固定SHAから新repoへソースと配布物を取り込み、元履歴参照とmanifestを作る。旧CI/deploy設定やsecretを機械的に持ち込まない。
2. gatewayとbase path対応を実装し、旧ゲームの挙動を保つ。Unity編集ソースを統合しない。
3. ローカルでRust/Node/gatewayを1サービスずつ検証する。全ページ・API・WebSocket、両Unityゲームのloader/data/wasm/Bundle/catalog、gzip/MIMEを確認する。
4. ブラウザでPong/Breakout/Dungeon/Fighting/Truckers/Canvas AirRace、AirRace3D、Colony Racerを確認する。2P/複数接続、入力、画面遷移、API/Bundle取得、持続接続を検証する。単なるHTTP200でゲーム動作正常としない。
5. GitHub repoの作成/反映と配備方式を決める。現在の初回禁止事項を解除せずcommit/push/PRやbuild/deployを実行したことにしない。
6. BASEの実パス・ポート・Compose・負荷・永続データ・既存domain管理を再確認し、公開切替の具体的な操作と戻し方をレビューする。新配置を公開前の別ポートで検証してから切り替える。
7. unity-games.wos.ktsys.jpを新gatewayへ切り替え、/01、/02、API互換経路、WebSocketと公開配布物を再確認する。既存proxy設定や旧containerへの変更はこの切替工程の対象として明示する。
8. 問題があればdomain経路を旧配置へ戻す。新Rust側でデータを書いた後の戻し方は事前に決める。受入れ前に旧repo/container/dataを削除しない。

## 成功条件と未確定事項

成功条件は、単一の配布repoから両店を再現できること、指定URLで全対象が動くこと、既存ゲームデータと配布物の整合性が保たれること、Unity元repoから新出力先が分かること、切替とrollbackの証拠が残ること。

未確定: BASEの新公開ポートと実マウント、既存proxyへ新gatewayを登録する具体的な方法、GitHub repoの可視性と配備設定、Rust永続データの実在と切替時の保全、旧domainを残す期間、各ゲームの実機QA範囲。これらは実物確認後に決め、現在の計画で稼働状態を上書きしない。


## 2026-10-11 追加: 共通入口・1号店のビルドと既存配備経路

ユーザーの最小整備GOに基づき、classic/gatewayの実Docker build CIと既存SSH→BASE側build経路を追加する。Unity成果物・image/containerとruntime6JSONを保持し、個別releaseタグと--no-depsで2サービスだけ更新する。詳細と停止条件はdocs/head/OPERATIONS.md。新鍵・runner・ネットワーク設定は追加しない。

PR #2マージ時点の記録: dev 25c625e3ba441655c33cf3e868cfca086cbd2088のDocker build CI run 38105519621とverify run 38105519655はsuccess。配備jobはliteral falseによってskippedで、その時点では新経路のBASE実行は未実施だった。

2026-10-11の仕上げでは、dev/BASE稼働版/信頼済みホスト鍵/保全基準を再確認。既存ssh base用dev鍵を秘密値非表示で暗号化登録し、新repoの接続設定6件を登録した。PR #3はliteral falseだけを解除し、dev限定・PR除外・有効化変数・strict known_hosts・最新SHA/clean fast-forward/flock・個別タグ・--no-depsを維持した。

devマージによるclassic/gatewayの自動配備と公開検証は1回成功した。配備後照合でSSH標準入力の消費による後続検証・タグ保存の未実行を発見し、health確認とタグ記録だけを補完。Unityのimage/container/114ファイル、runtime6JSON、対象外131コンテナ、routingを保持した。stdinを/dev/nullへ向ける1行修正と回帰テストはPR #4でCI成功後にdevへマージ済み。マージ時に配備変数を一時falseにして重複配備を防ぎ、devのDocker CI 38111146311とverify 38111146286のsuccess・deploy skippedを確認してtrueへ戻した。修正SHA ce2a22b9f25e60f9cd7e250f7afa35ba693d803d・文書commitと稼働image SHAを区別する。

