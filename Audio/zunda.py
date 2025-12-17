import requests
import sounddevice as sd
import soundfile as sf
import io

# ===== プロキシ回避（超重要）=====
SESSION = requests.Session()
SESSION.trust_env = False

BASE = "http://127.0.0.1:50021"

# -----------------------------
# ずんだもん speaker_id 取得
# -----------------------------
def get_zundamon_id(style_name="ノーマル"):
    speakers = SESSION.get(f"{BASE}/speakers").json()
    for sp in speakers:
        if sp["name"] == "ずんだもん":
            for st in sp["styles"]:
                if st["name"] == style_name:
                    return st["id"]
            return sp["styles"][0]["id"]
    raise RuntimeError("ずんだもんが見つからない")

# -----------------------------
# その場で喋らせる関数
# -----------------------------
def speak_now(text, style="ノーマル"):
    speaker_id = get_zundamon_id(style)

    # ① audio_query
    q = SESSION.post(
        f"{BASE}/audio_query",
        params={"text": text, "speaker": speaker_id},
        timeout=30
    ).json()

    # 🍯 ずんだもん温かみ設定（ぷーさん寄せ）
    q["speedScale"] = 0.9  # 話す速さ
    q["pitchScale"] = -0.1 # 声の高さ
    q["intonationScale"] = 0.3 # 抑揚（感情の起伏）
    q["prePhonemeLength"] = 0.10    # 音の前の間
    q["postPhonemeLength"] = 0.22   # 音の後の間

    # ② synthesis
    wav_bytes = SESSION.post(
        f"{BASE}/synthesis",
        params={"speaker": speaker_id},
        json=q,
        timeout=60
    ).content

    # ③ wavをメモリ上で再生（ファイル保存なし）
    with sf.SoundFile(io.BytesIO(wav_bytes)) as f:
        data = f.read(dtype="float32")
        sd.play(data, f.samplerate)
        sd.wait()  # 再生終了まで待つ

# -----------------------------
# 実行
# -----------------------------
if __name__ == "__main__":
    speak_now("ぼくはねぇきみとお話しできて、うれしいのー")
