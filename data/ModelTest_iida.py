# inference_only.py
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

VOCAB_SIZE = 5000
MAX_LEN = 30

# ===== 学習済み成果物をロード =====
model = load_model("emotion_model_regression.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# ===== 性格補正 =====
def apply_personality_bias(valence, arousal, text):
    valence += 0.05

    positive_hints = [
        "ラッキー", "よかった", "助かった", "安心",
        "余裕", "楽", "嬉しい", "いい"
    ]

    if any(word in text for word in positive_hints):
        valence += 0.05

    valence = max(min(valence, 0.6), -0.6)
    return valence, arousal

# ===== 推論関数 =====
def predict_emotion(text):
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN)
    val, aro = model.predict(x)[0]
    val, aro = apply_personality_bias(float(val), float(aro), text)
    return val, aro

# ===== テスト =====
while True:
    text = input("テキスト入力（exitで終了）: ")
    if text == "exit":
        break
    val, aro = predict_emotion(text)
    print(f"Valence: {val:.3f}, Arousal: {aro:.3f}")
