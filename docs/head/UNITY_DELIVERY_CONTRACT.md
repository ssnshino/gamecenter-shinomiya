# Unity成果物の新しい配置先

2026-10-11 JST: 統合repo作成、固定SHAからの取り込み、BASE配備と公開切替、HTTP/配布物/API/画面・基本操作を確認済み。Unityソースは既存repoに残し、Unity再ビルドは行っていない。

配布repo: `ssnshino/gamecenter-shinomiya.git`。
Mac: `/Volumes/SSD250GBUSB/source/repos/upstream/gamecenter-shinomiya`。
BASE: `/home/shino/source/repos/upstream/gamecenter-shinomiya`。

| 対象 | Unity編集元 | 新repo内の成果物path | 新公開URL |
|---|---|---|---|
| AirRace3D | ssnshino/airraceUnity | apps/unity-web/public/airrace3d | https://unity-games.wos.ktsys.jp/02/airrace3d/ |
| Colony Racer | ssnshino/colony-racer | apps/unity-web/public/colony-racer | https://unity-games.wos.ktsys.jp/02/colony-racer/ |

各成果物pathにindex.html、Build、TemplateData、StreamingAssetsを揃え、StreamingAssets/AirRaceにBundleとJSON catalogを置く。ソース、ビルド済み配布物、実公開状態はそれぞれ別に記録する。

AirRaceの出力先上書きはAIRRACE_WEBGL_BUILD_PATHを新airrace3d path、AIRRACE_STREAMING_SYNC_ROOTをそのStreamingAssets/AirRaceにする。ColonyはCOLONY_RACER_WEBGL_BUILD_PATHを新colony-racer path、COLONY_RACER_STREAMING_SYNC_ROOTをそのStreamingAssets/AirRaceにする。Unity editorの起動・再ビルド・既定値変更は行っていない。次回のビルド時は上記出力先を指定する。

既存compiledクライアントのドメイン直下API（/api/airrace3d/*、/api/colony-racer/*）は初回移行で互換経路を保つ。新しい/02/api/*だけに変更すると既存WebGLが使うcatalog URLを壊す可能性がある。

旧配布はssnshino/rust-sandbox/devで、Mac/BASEのcheckout名はunity-rust-games。旧URLの/airrace3d/と/colony-racer/は新/02配下へ308 redirectする。公開経路は切替済み、Unity builder既定pathは変更していない。unity-rust-games2は別AIRRACE3D2 stagingであり、今回の配布先ではない。


画面QAで、既存compiled resolverがURLの先頭segmentを使い /02/StreamingAssets/* を要求することを確認。gatewayはRefererの/02/airrace3d/または/02/colony-racer/を厳密に選び、対応するゲームだけへ配信する。Referer不明なら404。共有URLに別ゲームのcacheが混ざらないようprivate/no-storeとVary: Refererを付ける。正規の/02/<game>/StreamingAssets/*はReferer不要。Unity編集元の次回ビルドではresolverをサブパス対応にする候補だが、今回編集しない。
