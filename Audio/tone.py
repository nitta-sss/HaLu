import librosa
print("tone.py: STEP 6 librosa imported")
print("インストール開始")
import numpy as np
import os
print("np,osインストール完了")
USER_FILE = "users.txt"
DELTA_FULL = 80.0
THRESH_HZ = 25.0  # これ以上差があれば高い/低い判定


# -----------------------
# 音声 → 平均ピッチ(Hz)
# -----------------------
def get_mean_f0(y, sr=16000,flag=0):
    print("tone.py: STEP 5 inside get_mean_f0 (before librosa)")
    

    fmin = librosa.note_to_hz("C2")
    fmax = librosa.note_to_hz("C7")

    f0, _, _ = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sr)
    f0 = f0[~np.isnan(f0)]
    if len(f0) == 0:
        return None
    return float(np.mean(f0))


# -----------------------
# user.txt から「*付きユーザー」の平均Hzを取得
# 形式: 豪飛* 140
# -----------------------
def get_star_user_baseline(user_file=USER_FILE):
    if not os.path.exists(user_file):
        raise RuntimeError(f"{user_file} が見つかりません")

    with open(user_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                continue  # 壊れてる行はスキップ

            name_with_star = parts[0]
            hz_str = parts[1]

            if name_with_star.endswith("*"):
                name = name_with_star[:-1]  # *除去
                try:
                    baseline = float(hz_str)
                except ValueError:
                    raise RuntimeError(f"Hzが数値じゃない: {line}")
                return name, baseline

    raise RuntimeError("末尾に * が付いたユーザー行が見つかりません")


# -----------------------
# 相対トーン評価（*ユーザー基準）
# -----------------------
def analyze_tone_by_star_user(y, sr=16000):
    print("\n====== analyze_tone ======")

    star_name, baseline = get_star_user_baseline()
    print(f"⭐ 基準ユーザー: {star_name}")
    print(f"🎯 baseline: {baseline:.1f}Hz")

    current = get_mean_f0(y, sr)
    if current is None:
        raise RuntimeError("ピッチ取得失敗")

    print(f"🎤 今回の声のF0: {current:.1f}Hz")

    delta = current - baseline
    print(f"📏 delta = current - baseline = {delta:.1f}Hz")

    arousal = float(np.clip(delta / DELTA_FULL, -1.0, 1.0))
    print(f"🔥 arousal = {arousal:.2f}")

    if delta > THRESH_HZ:
        label = 0.05   # 高い
        verdict = "高い"
    elif delta < -THRESH_HZ:
        label = -0.05  # 低い
        verdict = "低い"
    else:
        label = 0      # ほぼ同じ
        verdict = "同じくらい"

    print(f"✅ 判定: {verdict}（label={label}）")
    print("=========================")

    return label
    #, verdict, current, baseline, delta, arousal

if __name__ == "__main__":
    print("tone.py: STEP 9 __main__ start")

    # ダミー波形（1秒ぶん）
    sr = 16000
    y = np.zeros(sr, dtype=np.float32)

    print("tone.py: STEP 10 calling analyze_tone_by_star_user...")
    try:
        out = analyze_tone_by_star_user(y, sr=sr)
        print("tone.py: STEP 11 analyze result =", out)
    except Exception as e:
        print("tone.py: STEP 11 ERROR:", e)
        import traceback
        traceback.print_exc()

    print("tone.py: STEP 12 __main__ end")
