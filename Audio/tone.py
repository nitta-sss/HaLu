import numpy as np
import json
import os

STORE_FILE = "voice_baseline.json"
DELTA_FULL = 80.0

# -----------------------
# 音声 → 平均ピッチ
# -----------------------
def get_mean_f0(y, sr=16000):
    # ★ ここでだけ librosa を読み込む（Flask起動を壊さない）
    import librosa

    fmin = librosa.note_to_hz("C2")
    fmax = librosa.note_to_hz("C7")

    f0, _, _ = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr)
    f0 = f0[~np.isnan(f0)]
    if len(f0) == 0:
        return None
    return float(np.mean(f0))


# -----------------------
# 保存ファイル操作
# -----------------------
def load_text():
    if not os.path.exists(STORE_FILE):
        return {}
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_text(data):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------
# ユーザー登録（なければ作る）
# -----------------------
def ensure_user(name, y, sr=16000):
    print(f"🔍 ensure_user() called for {name}")

    store = load_text()
    print("📂 現在の登録データ:", store)

    if name in store:
        print(f"ℹ {name} はすでに登録済み。baseline={store[name]:.1f}Hz")
        return store[name]

    print(f"🆕 {name} は未登録 → 今の音声で baseline を作成")

    f0 = get_mean_f0(y, sr)
    if f0 is None:
        raise RuntimeError("ピッチ取得失敗")

    store[name] = f0
    save_text(store)

    print(f"🎤 新規登録完了: {name} baseline={f0:.1f}Hz")
    return f0


# -----------------------
# 相対トーン評価
# -----------------------
def analyze_tone(name, y, sr=16000):
    print("\n====== analyze_tone ======")
    print("👤 user:", name)

    store = load_text()
    print("📂 登録データ:", store)

    # baseline がなければ、この音声で登録
    baseline = ensure_user(name, y, sr)
    print(f"🎯 使用する baseline: {baseline:.1f}Hz")

    current = get_mean_f0(y, sr)
    if current is None:
        raise RuntimeError("ピッチ取得失敗")

    print(f"🎤 今回の声のF0: {current:.1f}Hz")

    delta = current - baseline
    print(f"📏 delta = current - baseline = {delta:.1f}Hz")

    arousal = np.clip(delta / DELTA_FULL, -1.0, 1.0)
    print(f"🔥 arousal = {arousal:.2f}")

    if delta > 25:
        label = 0.05
    elif delta < -25:
        label = -0.05
    else:
        label = 0

    print(f"🏷 label = {label}")
    print("=========================")

    return label
