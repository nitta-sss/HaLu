# train_model.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import sqlite3
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import matplotlib.pyplot as plt

# DB取得
def load_data_db():
    conn = sqlite3.connect("AI.db")
    query = """
            SELECT t.テキストデータ, k.感情ID
            FROM TestData t 
            JOIN Emotion k ON t.感情ID = k.感情ID
            """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data_db()

# ----- Tokenizer -----
texts = df["テキストデータ"].values
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(texts)

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

seq = tokenizer.texts_to_sequences(texts)
X = pad_sequences(seq, maxlen=30)

# ----- 感情意味ベクトル -----
emotion_map = {
    0: {"valence": +0.8, "arousal": +0.4},
    1: {"valence": +0.9, "arousal": +0.6},
    2: {"valence": -0.8, "arousal": +0.8},
    3: {"valence": -0.7, "arousal": -0.6},
    4: {"valence":  0.0, "arousal":  0.0},
    5: {"valence": +0.1, "arousal": +0.9},
    6: {"valence": -0.3, "arousal": +0.3},
}

emotion_ids = df["感情ID"].astype(int).values

valence = np.array([emotion_map[i]["valence"] for i in emotion_ids])
arousal = np.array([emotion_map[i]["arousal"] for i in emotion_ids])
y_reg = np.vstack([valence, arousal]).T

# ----- モデル -----
model = Sequential([
    Embedding(input_dim=5000, output_dim=64, input_length=30),
    Bidirectional(LSTM(24, dropout=0.3, recurrent_dropout=0.3)),
    Dense(32, activation='relu'),
    Dropout(0.3),
    Dense(16, activation='relu'),
    Dropout(0.2),
    Dense(2, activation='tanh')
])

model.compile(
    optimizer=Adam(learning_rate=0.0005),
    loss="mse",
    metrics=["mae"]
)

history = model.fit(
    X, y_reg,
    epochs=50,
    batch_size=32,
    validation_split=0.2
)

# モデル保存
model.save("emotion_model.h5")
print("学習モデル保存完了（emotion_model_bilstm.h5）")
