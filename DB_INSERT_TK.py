# DB_INSERT_TK.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_PATH = "AI.db"

# 25マス：縦が arousal（a=0..4）、横が valence（p=0..4）
TABLE = [
    ["絶望😭", "しょんぼり🫩", "落ち込む😔", "満足🙂", "安心😀"],
    ["つらいけど平気🥲", "うるうる🥺", "無😑", "余裕😉", "うれしい😄"],
    ["不安🙁", "困惑😕", "ふつう😐", "にこにこ😊", "楽しい😆"],
    ["イライラ😠", "焦り😬", "ノリノリ😋", "上機嫌😚", "ハッピー🥰"],
    ["ブチギレ🤬", "怒り😡", "ハイテンション😁", "興奮🤩", "最高調🥳"],
]

def idx_to_vals(a, p):
    """
    p: 横（valence） 0..4 -> -1..1
    a: 縦（arousal） 0..4 -> -1..1
    """
    valence = (p - 2) / 2   # -1, -0.5, 0, 0.5, 1
    arousal = (a - 2) / 2   # -1, -0.5, 0, 0.5, 1
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

def get_total_and_counts():
    """
    return:
      total: int
      counts: dict {(aIdx, pIdx): count}
    """
    conn = sqlite3.connect(DB_PATH)
    ensure_table(conn)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM EmotionLog;")
    total = int(cur.fetchone()[0])

    cur.execute("""
        SELECT aIdx, pIdx, COUNT(*)
        FROM EmotionLog
        WHERE aIdx IS NOT NULL AND pIdx IS NOT NULL
        GROUP BY aIdx, pIdx
    """)
    rows = cur.fetchall()
    conn.close()

    counts = {(int(a), int(p)): int(cnt) for a, p, cnt in rows}
    return total, counts

class App(tk.Tk):
    def __init__(self, text=""):
        super().__init__()
        self.title("HaLu 感情ラベル入力")

        # 初期表示で下ボタンが見切れないように大きめ
        self.geometry("1200x780")
        self.minsize(1100, 720)
        self.resizable(True, True)

        # フォント
        self.FONT_TITLE = ("Meiryo", 18, "bold")
        self.FONT_BTN   = ("Meiryo", 16, "bold")
        self.FONT_TEXT  = ("Meiryo", 14)
        self.FONT_SMALL = ("Meiryo", 12)

        self.selected = None  # (a, p)
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

        # DB件数を読み込んでボタンに表示
        self.total_count, self.counts = get_total_and_counts()

        for a in range(5):
            for p in range(5):
                base = TABLE[a][p]
                cnt = self.counts.get((a, p), 0)
                label = f"{base}\n({cnt})"

                btn = tk.Button(
                    grid,
                    text=label,
                    font=self.FONT_BTN,
                    padx=12, pady=18,
                    wraplength=260,   # 文字つぶれ防止
                    justify="center",
                    command=lambda a=a, p=p: self.select(a, p)
                )
                btn.grid(row=a, column=p, padx=10, pady=10, sticky="nsew")
                self.buttons[(a, p)] = btn

        # ===== bottom =====
        # 左側：ステータス/件数情報
        left = tk.Frame(bottom)
        left.pack(side="left", fill="x", expand=True)

        self.info = tk.Label(
            left,
            text=f"総件数：{self.total_count} 件",
            font=self.FONT_SMALL,
            fg="black"
        )
        self.info.pack(anchor="w")

        self.status = tk.Label(
            left,
            text="未選択",
            font=self.FONT_TEXT,
            fg="gray"
        )
        self.status.pack(anchor="w", pady=(4, 0))

        # 右側：ボタン
        right = tk.Frame(bottom)
        right.pack(side="right")

        tk.Button(
            right,
            text="送信（保存）",
            font=self.FONT_BTN,
            width=14,
            bg="#4CAF50",
            fg="white",
            command=self.submit
        ).pack(side="right", padx=8)

        tk.Button(
            right,
            text="閉じる",
            font=self.FONT_TEXT,
            width=10,
            command=self.destroy
        ).pack(side="right", padx=8)

        # ===== ショートカット =====
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Return>", lambda e: self.submit())          # Enterで送信
        self.bind("<Control-Return>", lambda e: self.submit())  # Ctrl+Enterで送信
        self.bind("<BackSpace>", lambda e: self.clear_selection())  # Backspaceで選択解除（便利）

    def clear_selection(self):
        self.selected = None
        self.status.config(text="未選択", fg="gray")
        for (a, p), btn in self.buttons.items():
            btn.config(relief="raised", bg="SystemButtonFace")

    def refresh_counts(self):
        """DBから件数を再取得して、全ボタンの(件数)を更新"""
        self.total_count, self.counts = get_total_and_counts()
        self.info.config(text=f"総件数：{self.total_count} 件")

        for (a, p), btn in self.buttons.items():
            base = TABLE[a][p]
            cnt = self.counts.get((a, p), 0)
            btn.config(text=f"{base}\n({cnt})")

    def select(self, a, p):
        # まず全ボタンの見た目を戻す
        for btn in self.buttons.values():
            btn.config(relief="raised", bg="SystemButtonFace")

        # 選択ボタンだけ強調
        btn = self.buttons[(a, p)]
        btn.config(relief="sunken", bg="#FFD966")

        self.selected = (a, p)
        v, ar = idx_to_vals(a, p)
        cnt = self.counts.get((a, p), 0)

        self.status.config(
            text=f"選択中：{TABLE[a][p]}  (valence={v}, arousal={ar})  / このマス：{cnt}件",
            fg="black"
        )

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

        # 保存後：件数を即更新
        self.refresh_counts()

        # ステータス更新（ポップアップなし）
        self.status.config(
            text=f"✅ 保存OK：{label}  (v={valence}, a={arousal})",
            fg="green"
        )

        # 送信後：テキストを空に＆選択解除
        self.entry.delete(0, tk.END)
        self.clear_selection()
        self.entry.focus_set()

if __name__ == "__main__":
    import sys
    # 例: python DB_INSERT_TK.py "ラベル付けしたい文章"
    text = sys.argv[1] if len(sys.argv) >= 2 else ""
    App(text=text).mainloop()
