# Unity専用の自動配備（2026-10-15）

ユーザーのスマホ用デプロイ依頼と「自動デプロイ仕組みは入れてなかったけか」の指摘を受け、既存ActionsのBASE認証を使うUnity専用経路を追加する。Windowsへ鍵をコピーしない。既存classic/gateway自動配備はUnity差分を拒否するため流用しない。

対象はUnity workflow、既存Unity deploy/finalize/rollbackの呼出しwrapper、公開ブラウザsmoke、それらだけを許可する既存scope guardと回帰テスト・資料。既存のSecret/Variable・信頼済みhost keyを再利用し、鍵・runner・firewall・classic/gateway配備コードを変更しない。

devのColony成果物更新→manifest/テスト照合→SSHで固定SHAのUnityのみ暫定配備→公開HTTP/hash/APIと実ブラウザ6操作→既存finalizeでaccepted receipt。失敗時は既存のbounded rollbackを呼び、全体再配備やdata復元を行わない。PRでは認証を使うjobを実行しない。実source・配布SHA・image・実URL・receiptを区別して記録する。

成功条件は新成果物のlocal Edge/WebKit確認、Linux CI、公開ブラウザ受入れとaccepted receipt。自動配備job成功だけを実iPhone実測と扱わない。
