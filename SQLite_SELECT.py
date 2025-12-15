import sqlite3
import pandas as pd

# DB接続
conn = sqlite3.connect("AI.db")

# データ取得
df = pd.read_sql_query(
    """
    SELECT 感情ID, ROUND(AVG(valence),2), ROUND(AVG(arousal),2), COUNT(*)
    FROM TestData
    GROUP BY 感情ID
    ORDER BY 感情ID;
    """
    , conn)

conn.close()

# ===== 表示 =====
print("=== データ一覧 ===")
print(df)

print("\n=== 件数 ===")
print(len(df))
