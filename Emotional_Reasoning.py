#predict_emotion.py
# ---------------------------
# 1. Python標準ライブラリ
# ---------------------------
import time
from datetime import datetime
import threading
print("標準ライブラリimport完了")
# ---------------------------
# 2. 外部ライブラリ
# ---------------------------

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.losses import MeanSquaredError
print("外部ライブラリimport完了")


# Tokenizer 読み込み
try:
    with open("tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
        print("トークナイザー読み込み開始")
except Exception as e:
    print("❌ 読み込み 失敗")
    print(type(e), e)


# モデル読み込み
model = load_model("emotion_model_regression.h5",compile=False)
print("モデル読み込み完了")

model.compile(
    optimizer="adam",
    loss=MeanSquaredError(),      # ← 文字列"mse"禁止
    metrics=["accuracy"]          # ← mse は metrics に入れない
)

def predict_emotion(text):
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=30)
    pred = model.predict(x)[0]

    valence, arousal = pred[0], pred[1]
    return valence, arousal

# テスト実行
def suiron_test(text):
    val, aro = predict_emotion(text)

    return val, aro




