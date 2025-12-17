# speak.py
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
# JARVIS 音声パラメータ
# =========================
JARVIS_SPEAKER = 13        # 青山龍星（人間味あり）
JARVIS_SPEED = 1      # 少しゆっくり
JARVIS_PITCH = 0.12     # 下げすぎない
JARVIS_INTONATION = 0.5 # 抑揚を少し残す
JARVIS_VOLUME = 1.0


# =========================
# JARVIS エフェクト
# =========================
def add_echo(audio, delay=0.015, decay=0.18, sr=24000):
    delay_samples = int(sr * delay)
    echoed = np.zeros(len(audio) + delay_samples, dtype=np.float32)
    echoed[:len(audio)] += audio
    echoed[delay_samples:] += audio * decay
    return echoed



def jarvis_effect(audio, sr):
    """JARVIS用エフェクトまとめ"""
    audio = add_echo(audio, delay=0.025, decay=0.35, sr=sr)
    return audio


# =========================
# メイン：喋る関数
# =========================
def speak(text: str):
    if not text:
        return

    print("🤖 JARVIS speaking...")

    # --- プロキシ無視セッション ---
    session = requests.Session()
    session.trust_env = False

    # ① audio_query
    res = session.post(
        f"{VOICEVOX_URL}/audio_query",
        params={"text": text, "speaker": JARVIS_SPEAKER},
        timeout=3
    )
    query = res.json()

    # ② JARVIS用チューニング
    query["speedScale"] = JARVIS_SPEED
    query["pitchScale"] = JARVIS_PITCH
    query["intonationScale"] = JARVIS_INTONATION
    query["volumeScale"] = JARVIS_VOLUME

    # ③ synthesis
    audio = session.post(
        f"{VOICEVOX_URL}/synthesis",
        params={"speaker": JARVIS_SPEAKER},
        json=query,
        timeout=3
    )

    # ④ numpy配列に変換
    with io.BytesIO(audio.content) as f:
        audio_np, samplerate = sf.read(f, dtype="float32")

    # ⑤ JARVISエフェクト
    audio_np = jarvis_effect(audio_np, samplerate)

    # ⑥ 正規化（音割れ防止）
    audio_np /= np.max(np.abs(audio_np))
    audio_np = (audio_np * 32767).astype(np.int16)

    # ⑦ 一時WAVに書き出して再生（Windows標準）
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        sf.write(tmp.name, audio_np, samplerate, subtype="PCM_16")
        tmp_path = tmp.name

    winsound.PlaySound(tmp_path, winsound.SND_FILENAME)
    os.remove(tmp_path)


# =========================
# テスト
# =========================
if __name__ == "__main__":
    speak("システム起動。全モジュール、オンライン。")
