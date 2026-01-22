# ===============================
# Model_Emo.py (完全版)
# EmotionLog を使った感情回帰モデル（Janome対応 / 回帰）
# ===============================

import os
import random
import sqlite3
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from janome.tokenizer import Tokenizer as JanomeTokenizer


# ===============================
# 設定
# ===============================
DB_PATH = "AI.db"
TABLE_NAME = "EmotionLog"

VOCAB_SIZE = 5000
MAX_LEN = 40

EPOCHS = 80
BATCH_SIZE = 16

MODEL_PATH = "New_emotion_model_regression.h5"
TOKENIZER_PATH = "New_tokenizer.pkl"

# 学習ログ（グラフ保存先）
LOG_DIR = "train_logs"
os.makedirs(LOG_DIR, exist_ok=True)


# ===============================
# 乱数固定（再現性）
# ===============================
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


# ===============================
# Janome 分かち書き
# ===============================
_janome = JanomeTokenizer()

def wakati(text: str) -> str:
    # 念のためNone対策
    text = "" if text is None else str(text)
    return " ".join(t.surface for t in _janome.tokenize(text))


# ===============================
# DBからデータ取得
# ===============================
def load_data():
    abs_db = os.path.abspath(DB_PATH)
    if not os.path.exists(abs_db):
        raise FileNotFoundError(f"DBが見つかりません: {abs_db}")

    conn = sqlite3.connect(abs_db)
    df = pd.read_sql_query(
        f"""
        SELECT text, valence, arousal
        FROM {TABLE_NAME}
        WHERE valence IS NOT NULL
          AND arousal IS NOT NULL
          AND text   IS NOT NULL
          AND TRIM(text) <> ''
        """,
        conn
    )
    conn.close()

    print("✅ DB:", abs_db)
    return df


def print_distribution(df: pd.DataFrame):
    # ざっくり分布（5段階）
    def _bin(x):
        if x <= -0.6: return "[-1.0,-0.6]"
        if x <= -0.2: return "(-0.6,-0.2]"
        if x <  0.2:  return "(-0.2,0.2)"
        if x <  0.6:  return "[0.2,0.6)"
        return "[0.6,1.0]"

    v_bins = df["valence"].apply(_bin).value_counts()
    a_bins = df["arousal"].apply(_bin).value_counts()
    print("\n==== 分布チェック（5bin）====")
    print("valence bins:\n", v_bins.to_string())
    print("arousal bins:\n", a_bins.to_string())


# ===============================
# メイン
# ===============================
df = load_data()

print("\n==== EmotionLog 確認 ====")
print(df.head())
print("件数:", len(df))

if len(df) < 50:
    print("⚠ データが少なめです。valが暴れやすいので、まずは300件以上が目標。")

print_distribution(df)

# ===============================
# 前処理
# ===============================
texts_raw = df["text"].astype(str).values
texts = [wakati(t) for t in texts_raw]

y = df[["valence", "arousal"]].values.astype(np.float32)

# ===============================
# Tokenizer
# ===============================
tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)

with open(TOKENIZER_PATH, "wb") as f:
    pickle.dump(tokenizer, f)
print("✅ tokenizer 保存:", TOKENIZER_PATH)

X = tokenizer.texts_to_sequences(texts)
X = pad_sequences(X, maxlen=MAX_LEN)

print("X shape:", X.shape)
print("y shape:", y.shape)

# ===============================
# モデル定義（軽量版）
# ===============================
model = Sequential([
    Embedding(input_dim=VOCAB_SIZE, output_dim=64, input_length=MAX_LEN),

    # データ少なめ前提：LSTMは1段でOK
    Bidirectional(LSTM(32)),

    Dropout(0.3),
    Dense(16, activation="relu"),
    Dropout(0.3),

    Dense(2, activation="tanh")  # valence, arousal
])

# ラベルノイズに強い + 学習率低め
model.compile(
    optimizer=Adam(learning_rate=3e-4),
    loss=tf.keras.losses.Huber(delta=0.2),
    metrics=["mae"]
)

model.summary()

# ===============================
# 学習
# ===============================
callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=8,
        restore_best_weights=True
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-5,
        verbose=1
    )
]

history = model.fit(
    X, y,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=0.2,
    callbacks=callbacks,
    verbose=1
)

# ===============================
# 学習曲線（表示＋保存）
# ===============================
def save_plot(values, val_values, title, filename):
    plt.figure()
    plt.plot(values, label=title.lower())
    plt.plot(val_values, label="val_" + title.lower())
    plt.legend()
    plt.title(title)
    out_path = os.path.join(LOG_DIR, filename)
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.show()
    print("✅ 保存:", out_path)

save_plot(history.history["loss"], history.history["val_loss"], "Loss", "loss.png")
save_plot(history.history["mae"],  history.history["val_mae"],  "MAE",  "mae.png")

# ===============================
# 保存
# ===============================
model.save(MODEL_PATH)
print("✅ モデル保存:", MODEL_PATH)

# ===============================
# テスト推論（補正なし）
# ===============================
def predict_emotion(text: str):
    w = wakati(text)
    seq = tokenizer.texts_to_sequences([w])
    x = pad_sequences(seq, maxlen=MAX_LEN)
    val, aro = model.predict(x, verbose=0)[0]
    return float(val), float(aro)

test_texts = [
    "やったぁぁぁ！！内定決まった！！マジで嬉しすぎて叫びたい！！！",
    "特に何も感じない",
    "不安で落ち着かない",
    "ちょっとソワソワするけど悪いわけじゃない",
    "やる気が出てきて集中できそう"
]

print("\n==== 推論テスト ====")
for t in test_texts:
    v, a = predict_emotion(t)
    print(f"{t} -> valence={v:.2f}, arousal={a:.2f}")
