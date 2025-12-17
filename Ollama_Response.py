import subprocess

OLLAMA_PATH = r"C:\Users\232116\AppData\Local\Programs\Ollama\ollama.exe"

def llm_generate(user_text, timeout_sec=30):
    if not user_text or user_text.strip() == "":
        return None

    prompt = (
        "あなたは聞き役のAIです。"
        "次の発言に対して、自然な返答を1文だけ出してください。"
        f"発言: {user_text}"
    )

    try:
        result = subprocess.run(
            [
                OLLAMA_PATH,
                "run",
                "gemma3:1b",
                prompt
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",   # ★ここが超重要
            timeout=timeout_sec
        )
    except subprocess.TimeoutExpired:
        return None

    if result.returncode != 0:
        print("LLM error:", result.stderr)
        return None

    return result.stdout.strip() if result.stdout else None


# ===== テスト =====
if __name__ == "__main__":
    text = "開発成功してめっちゃうれしい！"
    reply = llm_generate(text)

    print("入力:", text)
    print("AI返答:", reply)
