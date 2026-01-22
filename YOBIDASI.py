# YOBIDASI.py
from data.emotion_inference import suiron_test
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result
from Audio.forest_paimon import speak
import time

last_reply = None


def _safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return float(default)


def run_ai(text=None):
    global last_reply
    print("結果受け取り")

    # text が無ければ音声認識結果
    if text is None:
        text = get_result()

    print("yoasobi:", text)

    if not text:
        # Flask/JSが落ちない形で返す
        return {
            "error": "テキストがありません",
            "text": "",
            "reply": "",
            "valence": 0.0,
            "arousal": 0.0
        }

    # -------------------------
    # 感情推論（user）
    # -------------------------
    print("感情推論開始")
    emo_user = suiron_test(text)
    print("感情推論できた", emo_user)

    # 壊れてても落ちない
    if not isinstance(emo_user, dict):
        emo_user = {}

    v = _safe_float(emo_user.get("valence", 0.0), 0.0)
    a = _safe_float(emo_user.get("arousal", 0.0), 0.0)

    # -------------------------
    # LLM 返答
    # -------------------------
    print("LLM呼び出し開始")
    try:
        last_reply = llm_generate(text)
    except Exception as e:
        print("❌ llm_generate error:", e)
        last_reply = ""

    last_reply = "" if last_reply is None else str(last_reply)
    print("LLM返答:", last_reply)

    # ※ AI側感情推論（Ollamaの返答）を使わないなら削除でOK
    # print("感情推論開始（reply）")
    # emo_reply = suiron_test(last_reply)
    # print("感情推論できた（reply）", emo_reply)

    return {
        "text": str(text),
        "valence": v,
        "arousal": a,
        "reply": last_reply
    }


def speak_ai(type):
    global last_reply
    print("発話開始")
    print(last_reply)
    print("🔊 speak called:", time.time())

    # last_reply が None のとき落ちないように保険
    speak(last_reply or "", type)

    print("🔊 speak finished:", time.time())
    print("発話終了")

    return {"status": "ok"}
