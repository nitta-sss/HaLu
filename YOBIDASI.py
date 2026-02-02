# YOBIDASI.py
from data.emotion_inference import suiron_test
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result_Hz
from Audio.forest_paimon import speak
from Audio.tone import analyze_tone_by_star_user
import time
import re

last_reply = None

def _split_japanese(text: str, max_len: int = 60):
    """
    句点/改行などで分割しつつ、max_len 目安でチャンク化
    """
    text = (text or "").strip()
    if not text:
        return []

    parts = re.split(r'(?<=[。！？\n])', text)

    chunks = []
    buf = ""
    for p in parts:
        p = p.strip()
        if not p:
            continue

        # 1文が長すぎるときは強制カット（保険）
        while len(p) > max_len:
            head, p = p[:max_len], p[max_len:]
            if buf:
                chunks.append(buf)
                buf = ""
            chunks.append(head)

        if len(buf) + len(p) <= max_len:
            buf += p
        else:
            if buf:
                chunks.append(buf)
            buf = p

    if buf:
        chunks.append(buf)

    return chunks


def _safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return float(default)


def run_ai(text=None):
    print("テキスト入力の処理")
    global last_reply
    print("結果受け取り")

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


def run_ai_voice(text=None):
    print("マイク入力の処理")
    global last_reply
    print("結果受け取り")

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

    Hz = get_result_Hz()
    print("HZ:",Hz)
    rivision = analyze_tone_by_star_user(Hz)
    print("補正値:",rivision)

    a += rivision
    print("補正結果：",a)

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
    text = (last_reply or "").strip()

    print("発話開始")
    print("全文:", text)
    print("🔊 speak called:", time.time())

    # 先頭は短く（発話開始を速く）
    first_chunks = _split_japanese(text, max_len=55)
    if not first_chunks:
        return {"status":"ok"}

    first = first_chunks[0]
    rest_text = text[len(first):].lstrip()

    rest_chunks = _split_japanese(rest_text, max_len=120)

    chunks = [first] + rest_chunks
    print(f"🧩 chunks={len(chunks)}")

    for i, ch in enumerate(chunks, 1):
        print(f"🔈 chunk {i}/{len(chunks)}:", ch)
        speak(ch, type)

    print("🔊 speak finished:", time.time())
    print("発話終了")
    return {"status":"ok"}




print("✅ YOBIDASI END (module finished)")
