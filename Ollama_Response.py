import subprocess
import shutil
from collections import deque

OLLAMA_PATH = shutil.which("ollama")
if OLLAMA_PATH is None:
    raise RuntimeError("Ollamaが見つからないヨ")

MODEL_NAME = "gemma3:1b"

# 会話履歴をグローバルで持つ（プロセスが生きてる間だけ記憶）
# {"role": "user" or "assistant", "content": "テキスト"}
conversation_history = deque()  # 必要なら maxlen=20 とかで上限つけてもOK


def build_conversation_prompt() -> str:
    """
    conversation_history から、LLM に渡す会話テキストを作る。
    """
    if not conversation_history:
        return ""

    # 重くなりすぎないように、直近 Nターンだけを使う
    MAX_TURNS = 6  # user+assistant のペアで6ターン分くらい
    recent = list(conversation_history)[-MAX_TURNS * 2:]  # role ごとに1メッセージなので×2

    lines = []
    for msg in recent:
        if msg["role"] == "user":
            lines.append(f"ユーザー: {msg['content']}")
        else:
            lines.append(f"AI: {msg['content']}")

    conversation_text = "\n".join(lines)

    # ★ここで中身を確認できる
    print("===== conversation_text =====")
    print(conversation_text)
    print("===== /conversation_text =====")

    return conversation_text


def llm_generate(user_text, timeout_sec=30):
    global conversation_history

    if not user_text or user_text.strip() == "":
        return None

    # まず、履歴にユーザー発話を追加
    conversation_history.append({
        "role": "user",
        "content": user_text.strip()
    })

    # 会話履歴からプロンプト用のテキストを作る
    conversation_text = build_conversation_prompt()

    # モデルに渡すプロンプト
    prompt = (
        "あなたは聞き役のAIです。\n"
        "これまでの会話履歴を踏まえて、最後のユーザーの発言に返答してください。\n"
        "日本語で、優しく自然な口調で、1〜3文程度で話してください。\n"
        "\n"
        "=== 会話履歴 ===\n"
        f"{conversation_text}\n"
        "\n"
        "AI:"
    )

    try:
        result = subprocess.run(
            [
                OLLAMA_PATH,
                "run",
                MODEL_NAME,
                prompt
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout_sec
        )
    except subprocess.TimeoutExpired:
        print("LLM timeout")
        return None

    if result.returncode != 0:
        print("LLM error:", result.stderr)
        return None

    reply = result.stdout.strip() if result.stdout else None

    if reply:
        # AI の返答も履歴に追加
        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

    return reply


# 会話リセットしたいとき用
def reset_conversation():
    conversation_history.clear()
    print("conversation_historyをリセットしました!")