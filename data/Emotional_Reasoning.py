#predict_emotion.py
# ---------------------------
# 1. Python標準ライブラリ
# ---------------------------
import time
from datetime import datetime
import threading

# ---------------------------
# 2. 外部ライブラリ
# ---------------------------
import pyaudio
import keyboard
from faster_whisper import WhisperModel

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from tensorflow.keras.losses import MeanSquaredError



# Tokenizer 読み込み
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# モデル読み込み
model = load_model("emotion_model.h5",compile=False)

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
def suiron_test():
    with open("C:/Users/232144/Desktop/HaLu/src/Audio/for_HaLu.txt", "rb") as f:
        text = pickle.load(f)
    val, aro = predict_emotion(text)

    print("入力文：", text)
    print("予測 Valence:", val)
    print("予測 Arousal:", aro)
    return val,aro


