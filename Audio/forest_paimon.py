import requests
import winsound
import tempfile
import os
import io
import numpy as np
import soundfile as sf

# =========================
# VOICEVOX 設定
# =========================
VOICEVOX_URL = "http://127.0.0.1:50021"

# =========================
# 森の妖精 音声パラメータ
# ※ speaker ID は変更しない
# =========================



# -------------------------
# 安全な pau モーラ
# -------------------------
def make_pau(vowel_length: float):
    return {
        "text": "pau",
        "consonant": None,
        "consonant_length": None,
        "vowel": "pau",
        "vowel_length": float(vowel_length),
        "pitch": 0.0
    }

PAUSE_SHORT = make_pau(0.14)
PAUSE_LONG  = make_pau(0.26)

def safe_add_pauses(query: dict) -> dict:
    aps = query.get("accent_phrases")
    if not isinstance(aps, list) or not aps:
        return query

    for i, ap in enumerate(aps):
        if ap.get("pause_mora") is not None:
            continue

        moras = ap.get("moras") or []
        if not moras:
            continue

        # 妖精はよく一息つく
        if type != "ice":
            if len(moras) >= 7:
                ap["pause_mora"] = PAUSE_SHORT
        else :
            print("一息なし")

        # 文末は深呼吸
        if type != "ice":
            if i == len(aps) - 1:
                ap["pause_mora"] = PAUSE_LONG
        else :
            print("深呼吸なし")

    query["accent_phrases"] = aps

    # 全体の間も少し長めに
    query["pauseLengthScale"] = 1.25
    query["prePhonemeLength"] = 0.10
    query["postPhonemeLength"] = 0.15
    return query

# -------------------------
# 森の残響エフェクト
# -------------------------
"""
def fairy_effect(audio, sr):
    delay = 0.045     # 少し遠くで反響
    decay = 0.22      # 優しい残り方
    delay_samples = int(sr * delay)

    effected = np.zeros(len(audio) + delay_samples, dtype=np.float32)
    effected[:len(audio)] += audio
    effected[delay_samples:] += audio * decay
    return effected
"""
def _synthesis(session, query, speaker: int):
    return session.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": speaker},
        json=query,
        timeout=10
    )

def speak(text: str,type):
    if not text or not str(text).strip():
        return

    
    if type == "forest":#まったりした優しい声
        print("🌿 妖精がそっと語りかけています…")
        FAIRY_SPEAKER=29
        FAIRY_SPEED = 0.90          # ゆったり
        FAIRY_PITCH = -0.11          # ほんのり高め
        FAIRY_INTONATION = 0.65     # なだらか
        FAIRY_VOLUME = 1.0

    elif type == "ice":#そっけないお姉さん
        print("🍧 妖精がそっと語りかけています…")
        FAIRY_SPEAKER = 78        # 冥鳴ひまり（クール寄り・安定）
        FAIRY_SPEED = 0.93       # ゆっくりめで落ち着き
        FAIRY_PITCH = -0.05      # 低めで冷静・大人っぽい
        FAIRY_INTONATION = 0.45  # 抑揚少なめ＝クール
        FAIRY_VOLUME = 0.94      # 控えめで透明感
        
    else:#flame　熱い若者
        print("🔥 妖精がそっと語りかけています…")
        FAIRY_SPEAKER = 11        # 青山劉生（低音・男声・安定）
        FAIRY_SPEED = 1.05       # 勢いはあるが重さを残す
        FAIRY_PITCH = -0.50      # しっかり低音
        FAIRY_INTONATION = 0.70  # 熱血だが叫びすぎない
        FAIRY_VOLUME = 1.08      # 前に出る迫力
        

    session = requests.Session()
    session.trust_env = False

    # ① audio_query
    res = session.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": FAIRY_SPEAKER},
        timeout=5
    )
    res.raise_for_status()
    query = res.json()

    # ② pause 調整
    query_pause = safe_add_pauses(dict(query))

    # ③ 音声パラメータ
    for q in (query_pause, query):
        q["speedScale"] = float(FAIRY_SPEED)
        q["pitchScale"] = float(FAIRY_PITCH)
        q["intonationScale"] = float(FAIRY_INTONATION)
        q["volumeScale"] = float(FAIRY_VOLUME)

    # ④ synthesis（pause入り優先）
    audio = _synthesis(session, query_pause, FAIRY_SPEAKER)
    if audio.status_code >= 500:
        audio = _synthesis(session, query, FAIRY_SPEAKER)

    audio.raise_for_status()

    # ⑤ numpy化
    with io.BytesIO(audio.content) as f:
        audio_np, sr = sf.read(f, dtype="float32")

    # ⑥ 妖精エフェクト
    #audio_np = fairy_effect(audio_np, sr)

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
    type="ic"
    speak("シンジ君がエヴァに乗らなくていいようにする",type)
