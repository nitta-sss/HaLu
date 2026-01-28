# YOBIDASI.py
print("YOBIDASI STEP 1: importing data.emotion_inference...")
from data.emotion_inference import suiron_test
print("YOBIDASI STEP 1 OK")

print("YOBIDASI STEP 2: importing Ollama_Response...")
from Ollama_Response import llm_generate
print("YOBIDASI STEP 2 OK")

print("YOBIDASI STEP 3: importing Audio.Voice_Read...")
from Audio.Voice_Read import get_result_Hz
print("YOBIDASI STEP 3 OK")

print("YOBIDASI STEP 4: importing Audio.forest_paimon...")
from Audio.forest_paimon import speak
print("YOBIDASI STEP 4 OK")

print("YOBIDASI STEP 5: importing tone...")
from Audio.tone import analyze_tone_by_star_user
print("YOBIDASI STEP 5 OK")

import time
print("YOBIDASI STEP 6: time imported OK")


last_reply = None


def _safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return float(default)


def run_ai(text=None):
    global last_reply
    print("結果受け取り")
    Hz=0
    # text が無ければ音声認識結果
    #if text is None:
    text,Hz = get_result_Hz()
    print("Hz:",Hz)

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

    if Hz is not None:
        print("感情補正入った")
        a_Hz = analyze_tone_by_star_user(Hz)
        print("補正結果：", a_Hz)
        a += a_Hz
    else:
        print("感情補正入れなかった")


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

    emo_AI=suiron_test(last_reply)
    AI_v = _safe_float(emo_AI.get("valence", 0.0), 0.0)
    AI_a = _safe_float(emo_AI.get("arousal", 0.0), 0.0)

    print("AI感情値：",AI_v,AI_a)

    # ※ AI側感情推論（Ollamaの返答）を使わないなら削除でOK
    # print("感情推論開始（reply）")
    # emo_reply = suiron_test(last_reply)
    # print("感情推論できた（reply）", emo_reply)

    return {
        "text": str(text),
        "valence": v,
        "arousal": a,
        "reply": last_reply,
        "AI_valence": AI_v,
        "AI_arousal": AI_a,
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
