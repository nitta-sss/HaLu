import requests
import winsound
import tempfile
import os
import io
import numpy as np
import soundfile as sf

VOICEVOX_URL = "http://127.0.0.1:50021"

JARVIS_SPEAKER = 21
JARVIS_SPEED = 1.15
JARVIS_PITCH = 0.05
JARVIS_INTONATION = 0.95
JARVIS_VOLUME = 1.0

# -------------------------
# 安全な pau モーラ
# -------------------------
def make_pau(vowel_length: float):
    # VOICEVOXが期待する pau はこれが一番事故りにくい
    return {
        "text": "pau",
        "consonant": None,
        "consonant_length": None,
        "vowel": "pau",
        "vowel_length": float(vowel_length),
        "pitch": 0.0
    }

PAUSE_SHORT = make_pau(0.10)
PAUSE_LONG  = make_pau(0.18)

def safe_add_pauses(query: dict) -> dict:
    aps = query.get("accent_phrases")
    if not isinstance(aps, list) or not aps:
        return query

    for i, ap in enumerate(aps):
        # 既に pause がある or moras が無いなら触らない
        if ap.get("pause_mora") is not None:
            continue
        moras = ap.get("moras") or []
        if not isinstance(moras, list) or len(moras) == 0:
            continue

        # 長い句だけ軽く切る（入れすぎないのが安定）
        if len(moras) >= 9:
            ap["pause_mora"] = PAUSE_SHORT

        # 最後の句は文末として少し長め
        if i == len(aps) - 1:
            ap["pause_mora"] = PAUSE_LONG

    query["accent_phrases"] = aps

    # 句読点由来の間も少しだけ整える（強くしすぎない）
    query["pauseLengthScale"] = 1.10
    query["prePhonemeLength"] = 0.07
    query["postPhonemeLength"] = 0.11
    return query

def jarvis_effect(audio, sr):
    # echo
    delay = 0.025
    decay = 0.35
    delay_samples = int(sr * delay)
    echoed = np.zeros(len(audio) + delay_samples, dtype=np.float32)
    echoed[:len(audio)] += audio
    echoed[delay_samples:] += audio * decay
    return echoed

def _synthesis(session, query, speaker: int):
    r = session.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": speaker},
        json=query,
        timeout=10
    )
    return r

def speak(text: str):
    if not text or not str(text).strip():
        return

    print("🤖 JARVIS speaking...")

    session = requests.Session()
    session.trust_env = False

    # ① audio_query
    res = session.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": JARVIS_SPEAKER},
        timeout=5
    )
    res.raise_for_status()
    query = res.json()

    # ② pause 自動挿入（安定版）
    query_pause = safe_add_pauses(dict(query))  # コピーして編集

    # ③ 声パラメータ
    for q in (query_pause, query):
        q["speedScale"] = float(JARVIS_SPEED)
        q["pitchScale"] = float(JARVIS_PITCH)
        q["intonationScale"] = float(JARVIS_INTONATION)
        q["volumeScale"] = float(JARVIS_VOLUME)

    # ④ synthesis（まず pause入りで試す → ダメなら通常にフォールバック）
    audio = _synthesis(session, query_pause, JARVIS_SPEAKER)
    if audio.status_code >= 500:
        # VOICEVOXが落ちた場合は、pause無しで再試行（必ず喋らせる）
        audio = _synthesis(session, query, JARVIS_SPEAKER)

    audio.raise_for_status()

    # ⑤ numpy化
    with io.BytesIO(audio.content) as f:
        audio_np, sr = sf.read(f, dtype="float32")

    # ⑥ エフェクト
    audio_np = jarvis_effect(audio_np, sr)

    # ⑦ 正規化
    peak = float(np.max(np.abs(audio_np))) if len(audio_np) else 0.0
    if peak > 0:
        audio_np = audio_np / peak
    audio_np = (audio_np * 32767).astype(np.int16)

    # ⑧ 再生
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio_np, sr, subtype="PCM_16")
        tmp_path = tmp.name

    winsound.PlaySound(tmp_path, winsound.SND_FILENAME)
    os.remove(tmp_path)

if __name__ == "__main__":
    speak("システム起動。全モジュール、オンライン。異常なし。")
