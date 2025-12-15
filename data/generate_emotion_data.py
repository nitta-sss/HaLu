import random
import sqlite3

# ===== 感情ごとの設計値 =====
EMOTION_CONFIG = {
    1: {  # 喜び
        "texts": [
            "本当に嬉しい", "やった、成功した", "思わず笑ってしまう",
            "最高の気分だ", "これは嬉しすぎる"
        ],
        "valence": 0.7,
        "arousal": 0.5
    },
    2: {  # 楽しい
        "texts": [
            "めちゃくちゃ楽しい", "テンション上がる", "ワクワクが止まらない",
            "楽しすぎる", "今が一番楽しい"
        ],
        "valence": 0.9,
        "arousal": 0.8
    },
    3: {  # 怒り
        "texts": [
            "ふざけるな", "本気で腹が立つ", "いい加減にしてほしい",
            "イライラが止まらない", "怒りで頭がいっぱいだ"
        ],
        "valence": -0.9,
        "arousal": 0.8
    },
    4: {  # 悲しみ
        "texts": [
            "とても悲しい", "気持ちが沈んでいる", "涙が出そうだ",
            "何もやる気が起きない", "胸が苦しい"
        ],
        "valence": -0.8,
        "arousal": 0.2
    },
    5: {  # 不安
        "texts": [
            "不安で落ち着かない", "嫌な予感がする", "心配で仕方ない",
            "この先が不安だ", "怖くて眠れない"
        ],
        "valence": -0.75,
        "arousal": 0.65
    },
    6: {  # 嫌悪
        "texts": [
            "気持ち悪い", "本当に無理", "見ていられない",
            "吐き気がする", "最悪な気分だ"
        ],
        "valence": -0.85,
        "arousal": 0.5
    },
    7: {  # 驚き
        "texts": [
            "え、マジで？", "信じられない", "そんなことある？",
            "予想外すぎる", "一瞬理解できなかった"
        ],
        "valence": 0.0,
        "arousal": 0.9
    }
}

# ===============================
# ② 生成数・揺らぎ設定
# ===============================

TARGET_COUNT_PER_EMOTION = 40   # ← 各感情の目標件数
VALENCE_NOISE = 0.08            # 揺らぎ
AROUSAL_NOISE = 0.08

import random
import sqlite3

# ===============================
# ① 感情設計
# ===============================
EMOTION_CONFIG = {
    1: {  # 喜び
        "texts": [
            "本当に嬉しい",
            "やった、成功した",
            "最高の気分だ",
            "思わず笑ってしまう",
            "これは嬉しすぎる"
        ],
        "valence": 0.7,
        "arousal": 0.5
    },

    2: {  # 楽しい
        "texts": [
            "めちゃくちゃ楽しい",
            "テンション上がる",
            "ワクワクが止まらない",
            "楽しすぎて時間忘れた",
            "今が一番楽しい"
        ],
        "valence": 0.9,
        "arousal": 0.8
    },

    3: {  # 怒り
        "texts": [
            "ふざけるな",
            "本気で腹が立つ",
            "いい加減にしてほしい",
            "イライラが止まらない",
            "怒りで頭がいっぱいだ"
        ],
        "valence": -0.9,
        "arousal": 0.8
    },

    4: {  # 悲しみ
        "texts": [
            "とても悲しい",
            "気持ちが沈んでいる",
            "涙が出そうだ",
            "何もやる気が起きない",
            "胸が苦しい"
        ],
        "valence": -0.8,
        "arousal": 0.2
    },

    5: {  # 不安
        "texts": [
            "不安で落ち着かない",
            "嫌な予感がする",
            "心配で仕方ない",
            "この先が不安だ",
            "怖くて眠れない"
        ],
        "valence": -0.75,
        "arousal": 0.65
    },

    6: {  # 嫌悪
        "texts": [
            "気持ち悪い",
            "本当に無理",
            "見ていられない",
            "吐き気がする",
            "最悪な気分だ"
        ],
        "valence": -0.85,
        "arousal": 0.5
    },

    7: {  # 驚き
        "texts": [
            "え、マジで？",
            "信じられない",
            "そんなことある？",
            "予想外すぎる",
            "一瞬理解できなかった"
        ],
        "valence": 0.0,
        "arousal": 0.9
    }
}


# ===============================
# ② 生成数・揺らぎ設定
# ===============================
TARGET_COUNT_PER_EMOTION = 40
VALENCE_NOISE = 0.08
AROUSAL_NOISE = 0.08

# ===============================
# ③ DBにINSERTする処理（←ここ）
# ===============================
conn = sqlite3.connect("AI.db")
cur = conn.cursor()

for emotion_id, cfg in EMOTION_CONFIG.items():
    for _ in range(TARGET_COUNT_PER_EMOTION):
        text = random.choice(cfg["texts"])

        valence = cfg["valence"] + random.uniform(-VALENCE_NOISE, VALENCE_NOISE)
        arousal = cfg["arousal"] + random.uniform(-AROUSAL_NOISE, AROUSAL_NOISE)

        # 範囲クリップ（tanh対策）
        valence = max(min(valence, 1.0), -1.0)
        arousal = max(min(arousal, 1.0), -1.0)

        cur.execute(
            """
            INSERT INTO TestData
            (発言者ID, テキストデータ, 感情ID, valence, arousal)
            VALUES (?, ?, ?, ?, ?)
            """,
            (1, text, emotion_id, valence, arousal)
        )

conn.commit()
conn.close()

print("✅ 感情データ INSERT 完了")
