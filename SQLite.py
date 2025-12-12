import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
INSERT INTO TestData (発言者ID, テキストデータ, 感情ID, valence, arousal) VALUES
(1,'少し手間はかかったけど、落ち着きを取り戻した',1,0.10,0.05)
""")




conn.commit()

conn.close()
