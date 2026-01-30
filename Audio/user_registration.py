from Audio.Voice_Read import get_result_Hz
from Audio.tone import get_mean_f0

USERS_FILE = "users.txt"

def registration_new(user):
    # --- トーン取得 ---
    y = get_result_Hz()
    Hz = get_mean_f0(y, flag=1)

    print("新規登録", user, "平均Hz", Hz)

    # --- user の * を除外した名前 ---
    user_clean = user.replace("*", "").strip()

    # --- 既存ユーザー読み込み ---
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        lines = []

    # --- 重複チェック ---
    for line in lines:
        parts = line.split()
        if not parts:
            continue

        name_raw = parts[0]              # 例: 蒼空*
        name_clean = name_raw.replace("*", "").strip()

        if name_clean == user_clean:
            print("❌ すでに同じユーザー名が存在します:", name_raw)
            return False   # 登録しない

    # --- かぶってなければ追記 ---
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{user_clean} {Hz}\n")

    print("✅ 登録完了:", user_clean, Hz)
    return True
