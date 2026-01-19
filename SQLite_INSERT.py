import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
DELETE FROM EmotionLog
""")




conn.commit()

conn.close()
