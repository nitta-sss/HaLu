import sqlite3
import pandas as pd

# DB接続
conn = sqlite3.connect("AI.db")

# データ取得
df = pd.read_sql_query(
    """
    SELECT COUNT(*) AS n
FROM EmotionLog
WHERE valence IS NOT NULL AND arousal IS NOT NULL;


    """
    , conn)

conn.close()

# ===== 表示 =====
print("=== データ一覧 ===")
print(df)

print("\n=== 件数 ===")
print(len(df))
