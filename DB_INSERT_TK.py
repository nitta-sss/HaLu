# DB_INSERT_TK.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "AI.db"

TABLE = [
    ["絶望😭","しょんぼり🫩","落ち込む😔","満足🙂","安心😀"],
    ["つらいけど平気🥲","うるうる🥺","無😑","余裕😉","うれしい😄"],
    ["不安🙁","困惑😕","ふつう😐","にこにこ😊","楽しい😆"],
    ["イライラ😠","焦り😬","ノリノリ😋","上機嫌😚","ハッピー🥰"],
    ["ブチギレ🤬","怒り😡","ハイテンション😁","興奮🤩","最高調🥳"],
]

def idx_to_vals(a, p):
    valence = (p - 2) / 2   # -1..1
    arousal = (a - 2) / 2   # -1..1
    return float(valence), float(arousal)

def ensure_table(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS EmotionLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            text TEXT NOT NULL,
            label TEXT NOT NULL,
            valence REAL NOT NULL,
            arousal REAL NOT NULL,
            aIdx INTEGER,
            pIdx INTEGER,
            source TEXT DEFAULT 'tk'
        );
    """)
    conn.commit()

class App(tk.Tk):
    def __init__(self, text=""):
        super().__init__()
        self.title("HaLu 感情ラベル入力")

        # ✅ 初期表示で下のボタンが見切れないように大きくする
        self.geometry("1200x780")     # ← ここ増やした
        self.minsize(1100, 720)       # ← ここ増やした
        self.resizable(True, True)

        # フォント
        self.FONT_TITLE = ("Meiryo", 18, "bold")
        self.FONT_BTN   = ("Meiryo", 16, "bold")
        self.FONT_TEXT  = ("Meiryo", 14)

        self.selected = None
        self.buttons = {}

        # ===== レイアウト：top / mid / bottom =====
        top = tk.Frame(self)
        top.pack(side="top", fill="x", padx=16, pady=14)

        mid = tk.Frame(self)
        mid.pack(side="top", fill="both", expand=True, padx=16, pady=(0, 12))

        bottom = tk.Frame(self)
        bottom.pack(side="bottom", fill="x", padx=16, pady=14)

        # ===== top =====
        tk.Label(top, text="テキスト（ラベル付け対象）", font=self.FONT_TEXT).pack(anchor="w")

        self.entry = tk.Entry(top, font=self.FONT_TEXT)
        self.entry.insert(0, text)
        self.entry.pack(fill="x", pady=10)
        self.entry.focus_set()

        tk.Label(top, text="感情を選択（25段階）", font=self.FONT_TITLE).pack(anchor="w")

        # ===== mid（グリッド）=====
        grid = tk.Frame(mid)
        grid.pack(fill="both", expand=True)

        for r in range(5):
            grid.grid_rowconfigure(r, weight=1)
        for c in range(5):
            grid.grid_columnconfigure(c, weight=1)

        for a in range(5):
            for p in range(5):
                label = TABLE[a][p]
                btn = tk.Button(
                    grid,
                    text=label,
                    font=self.FONT_BTN,
                    padx=12, pady=18,      # ✅ 少し大きく
                    wraplength=260,         # ✅ 文字つぶれ防止
                    justify="center",
                    command=lambda a=a, p=p: self.select(a, p)
                )
                btn.grid(row=a, column=p, padx=10, pady=10, sticky="nsew")
                self.buttons[(a, p)] = btn

        # ===== bottom =====
        self.status = tk.Label(bottom, text="未選択", font=self.FONT_TEXT, fg="gray")
        self.status.pack(side="left")

        tk.Button(
            bottom,
            text="閉じる",
            font=self.FONT_TEXT,
            width=10,
            command=self.destroy
        ).pack(side="right", padx=8)

        tk.Button(
            bottom,
            text="送信（保存）",
            font=self.FONT_BTN,
            width=14,
            bg="#4CAF50",
            fg="white",
            command=self.submit
        ).pack(side="right", padx=8)

        # ===== ショートカット =====
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self.submit())
        self.bind("<Control-Return>", lambda e: self.submit())
        self.bind("<BackSpace>", lambda e: self.clear_selection())

    def clear_selection(self):
        self.selected = None
        self.status.config(text="未選択", fg="gray")
        for btn in self.buttons.values():
            btn.config(relief="raised", bg="SystemButtonFace")

    def select(self, a, p):
        for btn in self.buttons.values():
            btn.config(relief="raised", bg="SystemButtonFace")

        btn = self.buttons[(a, p)]
        btn.config(relief="sunken", bg="#FFD966")

        self.selected = (a, p)
        v, ar = idx_to_vals(a, p)
        self.status.config(text=f"選択中：{TABLE[a][p]}   (valence={v}, arousal={ar})", fg="black")

    def submit(self):
        if not self.selected:
            messagebox.showwarning("未選択", "感情を選んでください")
            return

        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("空", "テキストを入れてください")
            return

        a, p = self.selected
        label = TABLE[a][p]
        valence, arousal = idx_to_vals(a, p)

        conn = sqlite3.connect(DB_PATH)
        ensure_table(conn)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO EmotionLog (text, label, valence, arousal, aIdx, pIdx, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (text, label, valence, arousal, a, p, "tk"))
        conn.commit()
        conn.close()

        # ✅ ポップアップ無しで保存結果だけ表示
        self.status.config(text=f"✅ 保存OK：{label}  (v={valence}, a={arousal})", fg="green")

        # ✅ 送信後：テキストボックスを完全に空にする
        self.entry.delete(0, tk.END)

        # 次の入力に備える：選択解除＆フォーカス
        self.clear_selection()
        self.entry.focus_set()

if __name__ == "__main__":
    import sys
    text = sys.argv[1] if len(sys.argv) >= 2 else ""
    App(text=text).mainloop()
