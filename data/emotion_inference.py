# data/emotion_inference.py
# ===============================
# 感情推論（補正なし・カテゴリー無し・安全版）
# ===============================

import pickle
from janome.tokenizer import Tokenizer as JanomeTokenizer
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ===============================
# 設定（学習時と一致）
# ===============================
MAX_LEN = 40

MODEL_PATH = "New_emotion_model_regression.h5"
TOKENIZER_PATH = "New_tokenizer.pkl"

# ===============================
# 読み込み
# ===============================
model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

# ===============================
# Janome 分かち書き（学習と同じ）
# ===============================
_janome = JanomeTokenizer()

def wakati(text: str) -> str:
    text = "" if text is None else str(text)
    return " ".join(t.surface for t in _janome.tokenize(text))

# ===============================
# 未知語だらけ判定
# ===============================
def is_unknownish(seq, tokenizer, threshold=0.7):
    if not seq:
        return True

    oov_id = tokenizer.word_index.get("<OOV>")
    if oov_id is None:
        # oov_token を使ってない場合は判定できないので「未知語扱いしない」
        return False

    oov_count = sum(1 for t in seq if t == oov_id)
    return (oov_count / max(1, len(seq))) >= threshold

# ===============================
# 推論（生出力のみ）
# ===============================
def predict_emotion(text):
    # 空入力 → ニュートラル
    if text is None or str(text).strip() == "":
        return 0.0, 0.0

    # 学習と同じ前処理
    w = wakati(text)
    seq = tokenizer.texts_to_sequences([w])[0]

    # tokenizerが理解できない → ニュートラル
    if is_unknownish(seq, tokenizer, threshold=0.7):
        print("⚠ unknown-ish -> neutral:", repr(text))
        return 0.0, 0.0

    x = pad_sequences([seq], maxlen=MAX_LEN)
    val, aro = model.predict(x, verbose=0)[0]
    return float(val), float(aro)

# ===============================
# 外部から呼ぶ関数（互換名）
# ===============================
def suiron_test(text):
    v, a = predict_emotion(text)
    return {"valence": v, "arousal": a}

if __name__ == "__main__":
    tests = [
        "今日はめっちゃ嬉しい",
        "特に何も感じない",
        "不安で落ち着かない",
        "",
        "asdfghjkl",
    ]
    for t in tests:
        print("text:", repr(t), "->", suiron_test(t))
