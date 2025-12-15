# ===============================
# 1. ライブラリ
# ===============================
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

import pickle
import numpy as np
print("AIインポート完了")
# ===============================
# 2. 定数
# ===============================
VOCAB_SIZE = 5000
MAX_LEN = 30
# ===============================
# 3. モデル & Tokenizer 読み込み
# ===============================
try:
    model = load_model("emotion_model_regression.h5")
    print("モデルOK")
except Exception as e:
    print("❌ モデル 読み込み失敗")
    print(type(e))
    print(e)
    raise

try:
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
except Exception as e:
    print("❌ tokenizer 読み込み失敗")
    print(type(e))
    print(e)
    raise


# ===============================
# 4. 性格補正
# ===============================
def apply_personality_bias(valence, arousal, text):
    """
    親しみやすい対話型AI用の性格補正
    """

    # 基本的に少し前向き
    valence += 0.05

    positive_hints = [
        "ラッキー", "よかった", "助かった", "安心",
        "余裕", "楽", "嬉しい", "いい"
    ]

    if any(word in text for word in positive_hints):
        valence += 0.05

    # 盛りすぎ防止
    valence = max(min(valence, 0.6), -0.6)

    return valence, arousal

# ===============================
# 5. 推論処理
# ===============================
def predict_emotion(text):
    #文字データ→数値データ
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN)

    #推論
    val, aro = model.predict(x, verbose=0)[0]

    #補正
    val, aro = apply_personality_bias(float(val), float(aro), text)
    return float(val), float(aro)

# ===============================
# 6. 外部から呼ぶ関数（入口）
# ===============================
def suiron_test_kari(text):
    val, aro = predict_emotion(text)
    return val, aro

# ===============================
# 7. 動作テスト
# ===============================
if __name__ == "__main__":
    test_text = "今日は電車が空いてて助かった"
    val, aro = suiron_test_kari(test_text)

    print("テキスト:", test_text)
    print("Valence:", val)
    print("Arousal:", aro)
