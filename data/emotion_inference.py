# ===============================
# 推論＋UI制御専用ファイル
# ===============================

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# ===============================
# 設定
# ===============================
MAX_LEN = 30

# ===============================
# モデル & tokenizer 読み込み
# ===============================
model = load_model("emotion_model_regression.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# ===============================
# 1. 生の感情推論（モデル）
# ===============================
def predict_emotion_raw(text):
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN)
    val, aro = model.predict(x, verbose=0)[0]
    return float(val), float(aro)

# ===============================
# 2. 象限判定（方向を決める）
# ===============================
def classify_quadrant(val, aro, v_th=0.12, a_th=0.45):
    if abs(val) < v_th and aro < a_th:
        return "neutral"

    if val >= v_th:
        if aro >= a_th:
            return "happy_excited"
        else:
            return "calm_positive"

    if val <= -v_th:
        if aro >= a_th:
            return "negative_excited"
        else:
            return "negative_calm"

    if aro >= a_th:
        return "surprised"

    return "neutral"

# ===============================
# 3. UI用ブースト（数値を盛る）
# ===============================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def boost_for_ui(raw_val, raw_aro, category):
    v = clamp(raw_val, -1.0, 1.0)
    a = clamp(raw_aro, 0.0, 1.0)

    if category == "happy_excited":
        v = max(v, 0.65)
        a = max(a, 0.70)

    elif category == "calm_positive":
        v = max(v, 0.40)
        a = clamp(a, 0.20, 0.45)

    elif category == "negative_excited":
        v = min(v, -0.55)
        a = max(a, 0.65)

    elif category == "negative_calm":
        v = min(v, -0.40)
        a = clamp(a, 0.10, 0.35)

    elif category == "surprised":
        v = clamp(v, -0.20, 0.20)
        a = max(a, 0.80)

    else:  # neutral
        v = clamp(v, -0.10, 0.10)
        a = clamp(a, 0.15, 0.35)

    return float(v), float(a)

# ===============================
# 4. セリフ決定
# ===============================
def decide_message(category):
    messages = {
        "happy_excited": "テンション上がってるね！",
        "calm_positive": "リラックスしてるよ。",
        "negative_excited": "ちょっと不安やイライラが強いかも。",
        "negative_calm": "気分が沈み気味かも…無理しないで。",
        "surprised": "びっくりした感じだね。",
        "neutral": "今はフラットな感じだよ。"
    }
    return messages.get(category, "今はフラットな感じだよ。")

# ===============================
# 5. 外部から呼ぶ唯一の関数
# ===============================
def suiron_test(text):
    raw_val, raw_aro = predict_emotion_raw(text)
    category = classify_quadrant(raw_val, raw_aro)
    ui_val, ui_aro = boost_for_ui(raw_val, raw_aro, category)
    message = decide_message(category)

    return {
        "valence": ui_val,     # ← グラフ表示用
        "arousal": ui_aro,     # ← グラフ表示用
        "category": category,  # ← 表情・演出用
        "message": message     # ← 吹き出し用
    }

if __name__ == "__main__":
    test = "嬉しい"

    raw_val, raw_aro = predict_emotion_raw(test)
    category = classify_quadrant(raw_val, raw_aro)
    ui_val, ui_aro = boost_for_ui(raw_val, raw_aro, category)

    print("text:", test)
    print("raw :", round(raw_val, 3), round(raw_aro, 3))
    print("cat :", category)
    print("ui  :", round(ui_val, 3), round(ui_aro, 3))
    print("msg :", decide_message(category))


