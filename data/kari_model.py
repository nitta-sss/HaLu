# ===============================
# 1. ライブラリ
# ===============================
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

import sqlite3
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# ===============================
# 2. DBから学習データ取得
# ===============================
def load_data_db():
    conn = sqlite3.connect("AI.db")
    df = pd.read_sql_query("""
        SELECT テキストデータ, valence, arousal
        FROM TestData
        WHERE valence IS NOT NULL
          AND arousal IS NOT NULL
    """, conn)
    conn.close()
    return df

df = load_data_db()

print("==== データ確認 ====")
print(df.head())
print("件数:", df.shape)

# ===============================
# 3. 入力（テキスト）と教師（回帰値）
# ===============================
texts = df["テキストデータ"].values
y_reg = df[["valence", "arousal"]].values  # ← 直接使う（超重要）

# ===============================
# 4. トークナイズ
# ===============================
VOCAB_SIZE = 5000
MAX_LEN = 30

tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)

with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

sequences = tokenizer.texts_to_sequences(texts)
X = pad_sequences(sequences, maxlen=MAX_LEN)

print("X shape:", X.shape)
print("y shape:", y_reg.shape)

# ===============================
# 5. モデル定義（回帰）
# ===============================
model = Sequential([
    Embedding(input_dim=VOCAB_SIZE, output_dim=64, input_length=MAX_LEN),

    Bidirectional(LSTM(32, return_sequences=True)),
    Bidirectional(LSTM(16)),

    Dense(32, activation="relu"),
    Dropout(0.3),

    Dense(16, activation="relu"),
    Dropout(0.2),

    Dense(2, activation="tanh")  # Valence, Arousal
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse",
    metrics=["mae"]
)

model.summary()

# ===============================
# 6. 学習
# ===============================
history = model.fit(
    X, y_reg,
    epochs=100,
    batch_size=16,
    validation_split=0.2,
    callbacks=[
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        )
    ]
)

# ===============================
# 7. 学習曲線
# ===============================
plt.plot(history.history["loss"], label="loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.legend()
plt.title("Loss")
plt.show()

plt.plot(history.history["mae"], label="mae")
plt.plot(history.history["val_mae"], label="val_mae")
plt.legend()
plt.title("MAE")
plt.show()

# ===============================
# 8. モデル保存
# ===============================
model.save("emotion_model_regression.h5")
print("✅ モデル保存完了")

# ===============================
# 9. テスト推論
# ===============================
def predict_emotion(text):
    seq = tokenizer.texts_to_sequences([text])
    x = pad_sequences(seq, maxlen=MAX_LEN)
    val, aro = model.predict(x)[0]
    return float(val), float(aro)

test_text = "今日は天気がいいので景色がよさそうだ"
val, aro = predict_emotion(test_text)

print("テキスト:", test_text)
print("予測 Valence:", val)
print("予測 Arousal:", aro)
