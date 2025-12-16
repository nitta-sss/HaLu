# ===============================
# 感情推論 + 感情メーター制御（最終完成版）
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
# ユーティリティ
# ===============================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

# ===============================
# 1. モデル生推論（数値はUI用）
# ===============================
def predict_emotion_raw(text):
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN)
    val, aro = model.predict(x, verbose=0)[0]
    return float(val), float(aro)

# ===============================
# 2. テキストの性質判定（カテゴリ専用）
# ===============================
def detect_strong_positive(text):
    return any(w in text for w in [
        "嬉しい","うれしい","楽しい","たのしい",
        "最高","幸せ","やった","めっちゃ"
    ])

def detect_calm_positive(text):
    return any(w in text for w in [
        "気分がいい","いい感じ","悪くない",
        "順調","落ち着く","天気がいい"
    ]) and not detect_strong_positive(text)

def detect_strong_negative(text):
    return any(w in text for w in [
        "不安","怖い","つらい","辛い",
        "嫌だ","最悪","イライラ","無理"
    ])

# ===============================
# 3. カテゴリ決定（※ arousalは使わない）
# ===============================
def classify_category(text, raw_val):
    if detect_strong_positive(text):
        return "happy_excited"

    if detect_calm_positive(text):
        return "calm_positive"

    if detect_strong_negative(text):
        return "negative_excited"

    if raw_val < -0.15:
        return "negative_calm"

    if abs(raw_val) < 0.15:
        return "neutral"

    return "calm_positive"

# ===============================
# 4. UI用 valence（固定しない）
# ===============================
def derive_ui_valence(text, raw_val, category):
    v = raw_val

    # 強調語
    if "めっちゃ" in text or "最高" in text:
        v += 0.15
    if "!" in text or "!" in text:
        v += 0.10

    if category == "happy_excited":
        v = max(v, 0.35)

    elif category == "calm_positive":
        v = max(v, 0.20)

    elif category == "negative_excited":
        v = min(v, -0.35)

    elif category == "negative_calm":
        v = min(v, -0.20)

    elif category == "neutral":
        v = clamp(v, -0.10, 0.10)

    return clamp(v, -1.0, 1.0)

# ===============================
# 5. UI用 arousal（演出専用）
# ===============================
def derive_ui_arousal(text, raw_aro, category):
    a = raw_aro

    # 強調
    if "!" in text or "!" in text:
        a += 0.15
    if "めっちゃ" in text:
        a += 0.15

    if category == "happy_excited":
        a = max(a, 0.75)

    elif category == "calm_positive":
        a = clamp(a, 0.25, 0.45)

    elif category == "negative_excited":
        a = max(a, 0.60)

    elif category == "negative_calm":
        a = clamp(a, 0.15, 0.35)

    elif category == "neutral":
        a = clamp(a, 0.15, 0.30)

    return clamp(a, 0.05, 1.0)

# ===============================
# 6. セリフ
# ===============================
def decide_message(category):
    return {
        "happy_excited": "テンション上がってるね！",
        "calm_positive": "穏やかでいい感じだね。",
        "negative_excited": "ちょっと不安やイライラが強いかも。",
        "negative_calm": "気分が沈み気味かも…無理しないで。",
        "neutral": "今はフラットな感じだよ。"
    }.get(category, "今はフラットな感じだよ。")

# ===============================
# 7. 外部から呼ぶ唯一の関数
# ===============================
def suiron_test(text):
    raw_val, raw_aro = predict_emotion_raw(text)

    category = classify_category(text, raw_val)

    ui_val = derive_ui_valence(text, raw_val, category)
    ui_aro = derive_ui_arousal(text, raw_aro, category)

    return {
        "valence": ui_val,     # 快楽度メーター
        "arousal": ui_aro,     # 覚醒度メーター
        "category": category,  # 感情カテゴリ
        "message": decide_message(category)
    }

# ===============================
# 8. 動作確認
# ===============================
if __name__ == "__main__":
    tests = [
        "明日バイト休みになってめっちゃうれしい",
        "今日は天気がいいので気分がいいです",
        "最高に気分がいいから嬉しい",
        "まあ悪くない一日だった",
        "正直ちょっと不安"
    ]

    for t in tests:
        print("\ntext:", t)
        print("→", suiron_test(t))
