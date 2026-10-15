<!-- IOS_SAFARI_BOOT_START -->
## 現在: iPhone Safariの起動クラッシュに対応（2026-10-15）

ユーザー実機でSafariが繰り返しクラッシュした。PC/WebKit smoke合格をiPhone適合と扱わない。対策版公開済み・iPhone実機の解消は未確認。約93MB→219MBのJS Brotli展開を、ブラウザnative展開へ変更。圧縮byte・展開後byteとUnityゲーム内容は同一。JS/WASMの.br MIMEを補正し、通常Edge/WebKitの確認を行った。機種・落ちる段階は確認待ち。原因はメモリ不足の可能性があり、断定していない。

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
  "artifactId": 11979271921
}
```

[Unity配信方式](https://docs.unity.com/en-us/engine/6000.5/manual/platform-specific/webgl/building-distribution/deploying)に従うnative Brotli transportの変更。実機メモリの直接計測はできていない。ゲームの常駐mesh/texture量を削減した修正ではない。次のWebGL生成で.unityweb fallbackへ戻さず、native圧縮ファイル名とContent-Encoding/MIMEを維持する。iPhone再確認で失敗する場合、モデル・iOS・起動段階と実機メモリを確認し、mobile用常駐資産を削減する。
