# Bouncer
簡単にバウンスアニメーションをつけることができるBlenderアドオンです。

This is a Blender add-on that allows you to easily add bounce animations.

# インストール / Installation
* Releasesからzipをダウンロード
* Edit > Preferences > Add-ons > Install from Disk からダウンロードしたzipを選択してインストール

---

* Download the zip file from Releases.
* Select the downloaded ZIP file via Edit > Preferences > Add-ons > Install from Disk.

# 使い方 / Usage
1. 3Dビューポート上のNパネル(Nキー)に"Bouncer"パネルが追加されます
2. プロパティをお好みのものに変更します
3. アニメーションさせたいオブジェクトを選択した状態で"Apply Animation"を押すと、設定したプロパティでキーフレームが打たれます

---

1. A "Bouncer" panel is added to the N-panel (N key) in the 3D viewport.
2. Change the properties to your preference.
3. When you press "Apply Animation" with the object you want to animate selected, keyframes are set based on the configured properties.

# プロパティ / Properties
* Transform Offset: トランスフォームのオフセット値
* Animation Settings
  * Use Current Frame: アニメーションの開始フレームに現在のフレームを使用するかどうか
  * Amplitude: バウンスの振幅
  * Period: バウンスの周期
  * Duration: アニメーションの長さ\[フレーム\]
  * Frame Offset: 複数のオブジェクトに適用した場合のフレームオフセット値\[フレーム\](アクティブオブジェクトからの距離に基づいてソートされます)

--- 

* Transform Offset: Transform Offset Value
* Animation Settings
  * Use Current Frame: Whether to use the current frame as the animation's start frame
  * Amplitude: Bounce Amplitude
  * Period: Bounce Period
  * Duration: Duration of Animation\[Frame\]
  * Frame Offset: Frame offset value when applied to multiple objects\[Frame\](Sorted by distance from the active object.)

# 互換性 / Compatibility
Blender5.0 or later
 
# ライセンス / Lisence
GPL v3.0
