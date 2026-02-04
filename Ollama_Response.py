import re
import subprocess
import shutil
from collections import deque

OLLAMA_PATH = shutil.which("ollama")
if OLLAMA_PATH is None:
    raise RuntimeError("Ollamaが見つからないヨ")

MODEL_NAME = "gemma2:2b"
conversation_history = deque()

# =========================
# ここに「決めた返答」を登録
# =========================

# 完全一致で返したい返答
FIXED_EXACT = {
    "こういう時、どんな顔すればいいのかわからないの": "笑えばいいと思うよ",
    "リセット": "了解！会話履歴をリセットするね。",
    "ヘルプ": "使い方：そのまま話しかけてOK。『リセット』で履歴を消せるよ。",
}

# 含まれてたら返したい返答（部分一致）
FIXED_CONTAINS = [
    ("りるか", "あぁ、そういうことね。五条りるかは俺が****。"),
]

# 正規表現で返したい返答
FIXED_REGEX = [
    (r"^/ping$", "pong"),
    (r"^/mode\s+(forest|ice|fire)$", "モード変更OK！そのテーマで喋るね。"),
]

def fixed_reply(user_text: str):
    """固定返答があれば文字列を返す。なければ None。"""
    t = (user_text or "").strip()
    if not t:
        return None

    # 1) 完全一致
    if t in FIXED_EXACT:
        return FIXED_EXACT[t]

    # 2) 部分一致
    for key, reply in FIXED_CONTAINS:
        if key in t:
            return reply

    # 3) 正規表現
    for pattern, reply in FIXED_REGEX:
        if re.search(pattern, t):
            return reply

    return None


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
    global conversation_history

    if not user_text or user_text.strip() == "":
        return None

    user_text = user_text.strip()

    # =========================
    # 先に「固定返答」を判定して返す
    # =========================
    fr = fixed_reply(user_text)
    if fr is not None:
        # 履歴に残したいなら残す（残したくないならこの2行消してOK）
        conversation_history.append({"role": "user", "content": user_text})
        conversation_history.append({"role": "assistant", "content": fr})

        # リセットみたいなコマンドもここで処理できる
        if user_text == "リセット":
            conversation_history.clear()
            return "conversation_historyをリセットしました!"

        return fr

    # 履歴にユーザー発話を追加（固定返答じゃない場合）
    conversation_history.append({"role": "user", "content": user_text})

    conversation_text = build_conversation_prompt()

    # 感情メタ情報
    emotion_block = ""
    if isinstance(emotion, dict):
        v = emotion.get("valence", None)
        a = emotion.get("arousal", None)
        cat = emotion.get("category", None)
        msg = emotion.get("message", None)

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
        "あなたの名前はパイモンです。Haluのメンバーによって感情が吹き込まれた寄り添いAIです。大事な要件を感情を込めて120字以内で話して。\n"
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
