# user_find.py

USERS_FILE = "users.txt"

def set_active_user(target_name: str):
    """
    users.txt の中で target_name にだけ * を付ける
    """
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        name = parts[0]
        hz = parts[1] if len(parts) > 1 else ""

        # 既存の * を消す
        name = name.replace("*", "")

        # 選択ユーザーなら * を付ける
        if name == target_name:
            name = name + "*"
            print("更新しました")

        new_lines.append(f"{name} {hz}\n")

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


# テスト用（単体実行したときだけ動く）
if __name__ == "__main__":
    user = input("選択するユーザー名を入力: ")
    set_active_user(user)
    
