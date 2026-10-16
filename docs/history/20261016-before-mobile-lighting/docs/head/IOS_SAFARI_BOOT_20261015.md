<!-- CITY_DIAGNOSTIC_ACCEPTED_START -->
## 現在: 市街地切り分け版がiPhone 17で起動・走行（2026-10-16）

Unity source d30013583556733cadb80d1cb043af65272c7d5e、配布release/Unity RELEASE_TAG8c0b9e52590ad0ff00c534f55522012bc278579e。Actions38846295459 success、公開9checks/6operationsとreceipt accepted/adoptionComplete true/exitCode0を確認。iPhone 17で開始画面・走行の実機確認あり。写真HUD118〜120km/h・接地、軽量26〜30fps/詳細34fpsはその時点の表示で持続性能保証ではない。

高速道路・環状線/IC/JCT・長距離地上道・山/追加景観地形をcity-diagnosticで一時オミット。市街地3地区・元の橋・鉄骨・安全内壁/採光帯・街区LODは保持。data57,351,365bytes/展開後100,916,295bytes。ローカルEdge22/WebKit21 PASS。通常/診断/再読込/通常復帰の生成検証もPASS。元データは保存されfullへ切替可能。

URL: https://unity-games.wos.ktsys.jp/02/colony-racer/?v=city-diagnostic-20261016 。前便forest版も実機では起動前クラッシュした。今回写真では遠方白飛び・近景の平坦さが残り、軽量/詳細切替でも改善しない。照明調整は次便であり、今回の受入れに含めない。Windows Editor再生成/Play確認もWebの成功と区別する。

詳細: docs/head/CITY_DIAGNOSTIC_WEB_20261016.md。更新前入口資料はdocs/history/20261016-before-city-diagnostic-acceptanceにexact bytes/hashで保全。以下は過去状態の記録。
<!-- CITY_DIAGNOSTIC_ACCEPTED_END -->

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

```json
{
  "unitySourceSha": "eeca3f261038b6d6bf271b91157b0a5abf23ac9d",
  "airRaceUnchanged": true,
  "legacyColonyAssetsUnchanged": true,
  "changes": [
    {
      "old": "039797c5b50e282a6830e1ba3395b666.data.unityweb",
      "next": "039797c5b50e282a6830e1ba3395b666.data.br",
      "compressedBytes": 92787516,
      "rawSha256": "457db986715edeb01506675710534b920302522922f5f2638944f7ab7fdbb7c7",
      "decodedBytes": 218766927,
      "decodedSha256": "7ba1ef3cc83180b02f39687df4fd80cf4765c23297098230f626e6c8ac5d7598"
    },
    {
      "old": "cddf0eba65e9799f3cf3cfd83d2b5db7.framework.js.unityweb",
      "next": "cddf0eba65e9799f3cf3cfd83d2b5db7.framework.js.br",
      "compressedBytes": 77224,
      "rawSha256": "d35268923e9f711fb29d403a785185fc4ba8be39387c3a3674670ed976d60a1d",
      "decodedBytes": 432864,
      "decodedSha256": "280ca46233d864218df876ea572114b1d06a594e4ece5519c965ecffe4f01b8c"
    },
    {
      "old": "d2064f885915dfe8c239fc3316c08ff2.wasm.unityweb",
      "next": "d2064f885915dfe8c239fc3316c08ff2.wasm.br",
      "compressedBytes": 5350114,
      "rawSha256": "fda4b87aab24fb2344d39f55a0c8b96acdb5763c9ca571dcc773425e6ef6c48f",
      "decodedBytes": 19964362,
      "decodedSha256": "cc21057bd6b871901a658b25adb35abae79ea7ea0a31021ec2b5351b0cf49373"
    }
  ],
  "distributionCandidate": "db6b78b7631800b6b16fa9bcb6ba4239eda84a7e",
  "reportedIPhoneCrash": true,
  "actualPhoneFixConfirmed": false,
  "localEdgeChecks": 25,
  "localWebKitChecks": 24,
  "publicWebKitChecks": 24,
  "publicHeaders": "ios-native-brotli-public-headers.json",
  "run": 38745949087,
  "runtimeSourceUnchanged": true,
  "nativeWasmHeaderVerified": true,
  "accepted": true,
  "acceptedUtc": "2026-10-15T13:58:55Z",
  "distributionSha": "db6b78b7631800b6b16fa9bcb6ba4239eda84a7e",
  "imageId": "sha256:d928cb12a1439ea451ecc92fa14eb1b7fd9fd23a030678c06b5f042f2f8fd16e",
  "receipt": "runtime/deploy/unity-colony-db6b78b7631800b6b16fa9bcb6ba4239eda84a7e-20261015T135010Z",
  "artifactId": 11979271921,
  "reportedDevice": "iPhone 17",
  "reportedCrashStage": "before start button appears"
}
```

[Unity配信方式](https://docs.unity.com/en-us/engine/6000.5/manual/platform-specific/webgl/building-distribution/deploying)に従うnative Brotli transportの変更。実機メモリの直接計測はできていない。ゲームの常駐mesh/texture量を削減した修正ではない。次のWebGL生成で.unityweb fallbackへ戻さず、native圧縮ファイル名とContent-Encoding/MIMEを維持する。iPhone再確認で失敗する場合、モデル・iOS・起動段階と実機メモリを確認し、mobile用常駐資産を削減する。
