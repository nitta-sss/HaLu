import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
INSERT INTO TestData (発言者ID, テキストデータ, 感情ID, valence, arousal)
               

""")




conn.commit()

conn.close()
