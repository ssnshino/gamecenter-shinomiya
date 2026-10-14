# Colony Racer 既存街並みの外観更新（2026-10-15）

Coreの無窓の箱、均一な窓、道路と縁石の同じ材質を修正したUnityのWebGL成果物。既存Core／East／West、道路・区画、固定構造856、P0-P2車体とPC／touch入力を継続する。Unity編集元はssnshino/colony-racer、今回の実コードcommitは `a5c3493a9378480e24a54b99bfe169662fbf028b`、build SourceIdはsource-input-final-r2.jsonの102fd09。生成物を編集ソースの代わりにしない。

42共有模型／84LOD、窓・入口・屋根設備、白線の受影と局所摩耗、独立縁石、補修9／土境界6、葉の光を追加。Web AOは実画像の利得と費用を比較して既定OFF、shadow bias0.05／normal0.12。元の形状・Collider digestと原scene/prefabのbyteは保持する。提供写真10は私的な参考で、JPG・logo・車種を配布へ含めない。

Unity6000.4.3f1、OpenGLES3／ETC2／Gzip fallback／DiskSizeLTO、errors0／warnings274。Colony58 files／58,567,693bytes。AirRace57、Colony StreamingAssets37／TemplateData14はbyte不変。Node配信、Rust、Compose、gateway、workflow、runtime dataは変更しない。

ローカル実検証: Core/East/West×詳細/軽量＋AO depth復元で9測定・10PNG、独立158項PASS。PC24／touch33／WebKit31の88checks・884samples。120km/h近傍への加速、制動、左右操舵、地区移動・reset・入力解除を確認。Web高速時の連続接地gateはfalse、iPhone実機は未測定。focusはsynthetic blur handler検査で、OS focus喪失は未確認。Native先行7視点と、最終同source Core近景1視点（59.5448fps）を区別する。Web詳細Core44.959fpsで旧before60.264より低く、常時60fpsは保証しない。

調査・結果はUnity sourceの docs/head/STREETSCAPE_REALISM_RESEARCH_20261015.md／STREETSCAPE_REALISM_20261015.md。rawは `/Volumes/SSD250GBUSB/source/validation/colony-racer/20261015-streetscape-realism`。source-commit.jsonは1410入力のうちtracked1404／ignored既存6を区別し、実package/settings・build・artifactへ対応する。

公開先は [従来URL](https://unity-games.wos.ktsys.jp/02/colony-racer/)。この文書・mergeを公開完了の証拠にしない。[Unity限定手順](COLONY_WEBGL_PUBLICATION.md)でUnity imageだけ暫定更新し、公開115assetのhash/gzip/MIME/catalogとPC/touch実操作を確認し、receipt acceptedと永続RELEASE_TAG・live imageを照合する。source commit、配布commit、稼働image、文書だけの後続commitを区別する。対象外container・runtime6JSON・routingを保持する。
