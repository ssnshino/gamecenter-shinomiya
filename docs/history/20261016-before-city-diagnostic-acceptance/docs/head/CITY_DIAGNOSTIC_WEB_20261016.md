# 市街地中心のiPhone起動切り分け版

森林なし公開版でもiPhone 17は開始前に落ちる、とユーザー実機で確認。高速道路/山/N-S方面直線道路を一時的に外し、すぐ復帰できる版を依頼された。今回の公開は診断用であり、iPhone修正成功とは扱わない。

Unity source: d30013583556733cadb80d1cb043af65272c7d5e。`city-diagnostic` をシーンへベイク。生成しない: 軸高架・環状線・IC/JCT・地上長距離道・関連中央分離帯/標識/予約敷地・山/草原/造成地。市街地3地区・元の橋・鉄骨・内壁安全支持・採光帯・街区LOD・街路樹は保持。森林は既存OFF。

通常→診断→再読込→通常復帰PASS。Infrastructure mesh2737→767、Collider7979→482、山/地形89→0、追加道路判定1356→0。鉄骨240/内壁525mesh、市街地4627meshの名前/頂点数/局所位置/scaleの比較hash一致。元のScene/Prefab SHA256保持。

Web Build Succeeded/errors0/warnings286（再コンパイルに伴う既存API非推奨警告等を含む）。native Gzip/fallback false/ETC2/GLES3/DiskSizeLTO、initial256/max1024MB、wasm2023=falseを継続。data配信57,351,365bytes/展開後100,916,295bytes（前便84,612,569/162,904,246）。data decoded SHA256 02d80786f5c22ae50258b0563112dfd8f5680047af7b3a56e70f7c88769fcf32。visual mesh CPU copy除外285、forest compressed0。

ローカルEdge22/WebKit21 checks PASS。開始・3地区・縦横touch・加速/制動/操舵/復帰・省略道路ボタン非表示を確認。CIは明示的なcityDiagnostic telemetry時のみ道路移動の代わりに非表示/無効化を確認し、通常版の道路試験は保持。256px software CIを実機性能の証拠にはしない。AirRace/保持catalog/Bundle/StreamingAssets/TemplateDataの一致をmanifestで確認。

配備は既存のUnity専用Actionsを使い、guard→仮配備→公開ブラウザ→acceptedの順。公開採用は進行中。予定URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=city-diagnostic-20261016

復帰: UnityはCOLONY_SCENERY_PROFILE=fullで再生成。Editorメニュー（source follow-up）はColony Racer > Diagnostics > Restore Full Scenery。公開の直前生成済みWebGLはrelease f75d8649bb6112326355c45b26f91bd66265f228に保存済みで、Unity再ビルドなしにGit復元/再配備できる。
