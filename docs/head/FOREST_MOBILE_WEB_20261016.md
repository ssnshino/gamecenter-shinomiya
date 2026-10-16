# 森林なし・街区LOD版のスマホ再試走用公開（2026-10-16）

現段階は候補。accepted receipt確認までは旧公開版を採用済みとして扱う。

Unity source: a02c3ae8909e02084a2d44ee7fb2ab6aa19cebc8。ランタイムはd1502bcの森林なし/街区LODと同じ。Editor builderにnative-gzip profileだけ追加。Unity 6000.4.3f1でBuild Succeeded、errors0/warnings22、元Scene/Prefab SHA-256保持。Gzip / decompressionFallback=false / DiskSizeLTO / ETC2 / GLES3 / wasm2023=false / initial256MB / max1024MB。森林mesh圧縮対象0。生成装飾1,278meshはGPUのみの保持。

ゲームdataはgzip 84,612,569bytes、HTTP展開後162,904,246bytes（前便native Brotliは92,787,516 / 218,766,927bytes）。Wasm gzip6,934,787 / raw19,979,554bytes。内容・画質・山/道路/JCT/車両物理を変更する圧縮ではない。配信は既存Content-Encoding:gzip/JS/WASM MIME対応を使用し、JSでの追加展開は使わない。

最初のBrotli試行はリンク完了後のdata圧縮が入力約半分で20分以上となったため、検証した隔離workerだけを止めた。失敗reportのoriginalSceneUnchanged/originalPrefabUnchangedはtrue。gzip比較163,060,694→86,233,107bytesは35.44秒で終わり、GitHub100MiB制限内だったため正式native-gzipビルドへ切替えた。初回Brotliが成功したことにはしない。

元Unity作業場の6材質の実行時Emission keyword差分とPackages2差分は保護。ビルドコピーの材質はsource commitのbyteを使い、残る入力と共にsource inventoryへ記録。既存AirRaceの全file byteとColonyのStreamingAssets/TemplateDataを比較保持。ColonyのBuild/index/manifestだけ更新する。

local Edge/WebKitの起動・タッチUI・高架/3環状/3地区・加速/制動/操舵/reset/pauseの確認を進め、既存自動配備で公開ブラウザ→receipt finalize。LAN Git bundle prefetchは既存Actions鍵でBASEへgit objectと専用交渉refだけを取り込み、checkout/servicesを変更せず、その後のdev fetchに再利用する。

証拠はこのPCの C:/Users/shino/Documents/Codex/2026-10-15/c/outputs/forest-web-*。PC/WebKit smokeは実iPhone 17の起動成功を保証せず、実機は公開後ユーザー検証待ち。
