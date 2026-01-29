from Audio.Voice_Read import get_result_Hz
from Audio.tone import get_mean_f0

def reload_Hz(user):
    USERS_FILE="users.txt"
    print("クリーン前",user)
    user_clean = user.replace("*", "")
    print("選択ユーザー",user_clean)
    y = get_result_Hz()
    print(y)
    Hz = get_mean_f0(y,flag=1)
    print("平均トーン",Hz)

    # ファイル読み込み
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    print("retake ファイル読み込み完了")

    new_lines = []

    for line in lines:
        parts = line.split()
        if not parts:
            new_lines.append(line)
            continue

        name_raw = parts[0]                   # 蒼空*
        name_clean = name_raw.replace("*", "")  # 蒼空

        print("name_clean",name_clean)



        if name_clean == user_clean:
            new_lines.append(f"{name_raw} {Hz}")
        else:
            new_lines.append(line)

    # ファイルに書き戻し
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))
    
    print("ファイル更新完了",new_lines)
    