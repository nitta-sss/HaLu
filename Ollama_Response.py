import subprocess
import shutil
from collections import deque

OLLAMA_PATH = shutil.which("ollama")
if OLLAMA_PATH is None:
    raise RuntimeError("Ollamaが見つからないヨ")

MODEL_NAME = "gemma3:1b"

conversation_history = deque()

def build_conversation_prompt(max_turns=6) -> str:
    if not conversation_history:
        return ""

    recent = list(conversation_history)[-max_turns * 2:]
    lines = []
    for msg in recent:
        if msg["role"] == "user":
            lines.append(f"ユーザー: {msg['content']}")
        else:
            lines.append(f"AI: {msg['content']}")
    return "\n".join(lines)

def llm_generate(user_text, emotion=None, timeout_sec=30):
    """
    emotion: suiron_test(text) の dict を想定
      {
        "valence": float,
        "arousal": float,
        "category": str,
        "message": str
      }
    """
    global conversation_history

    if not user_text or user_text.strip() == "":
        return None

    user_text = user_text.strip()

    # 履歴にユーザー発話を追加
    conversation_history.append({"role": "user", "content": user_text})

    conversation_text = build_conversation_prompt()

    # 感情メタ情報（今回ターン用の補助）
    emotion_block = ""
    if isinstance(emotion, dict):
        v = emotion.get("valence", None)
        a = emotion.get("arousal", None)
        cat = emotion.get("category", None)
        msg = emotion.get("message", None)

        # 値を見やすく（丸め）
        def fmt(x):
            try:
                return f"{float(x):+.2f}"
            except Exception:
                return str(x)

        emotion_block = (
            "\n"
            "=== 感情推論（今回のユーザー発話）===\n"
            f"- category: {cat}\n"
            f"- valence: {fmt(v)}（快楽度: -1〜+1）\n"
            f"- arousal: {fmt(a)}（覚醒度: 0〜1）\n"
            f"- system_message: {msg}\n"
            "※この情報は返答のトーン調整のみに使い、ユーザーには数値やカテゴリを直接言わない。\n"
        )

    prompt = (
        "あなたの名前はパイモンです。大事な要件を120字以内で話して。"
        "=== 会話履歴 ===\n"
        f"{conversation_text}\n"
        
        f"{emotion_block}\n"
        "AI:"
    )

    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", MODEL_NAME, prompt],
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
        conversation_history.append({"role": "assistant", "content": reply})

    return reply

def reset_conversation():
    conversation_history.clear()
    print("conversation_historyをリセットしました!")
