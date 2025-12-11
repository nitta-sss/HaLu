import pyaudio
import numpy as np
import wave
import time
from datetime import datetime
from faster_whisper import WhisperModel
import threading
import keyboard

recording = False
audio_buffer = []
lock = threading.Lock()
stop_flag = False
final_text = None  # ← ここに最終テキストを保存する

# -----------------------------
# 設定
# -----------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK = 1024
TEMP_WAV = "temp.wav"

# Whisperモデル
model = WhisperModel("small", device="cpu", compute_type="int8")

# -----------------------------
# 音声認識
# -----------------------------
def transcribe_audio(path):
    segments, info = model.transcribe(path, beam_size=3, language="ja")
    return "".join([seg.text for seg in segments])

# -----------------------------
# バッファ処理 → WAV保存 → Whisper
# -----------------------------
def process_buffer():
    global audio_buffer, final_text, stop_flag

    if not audio_buffer:
        return

    # WAV保存
    with wave.open(TEMP_WAV, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(audio_buffer))

    # Whisper変換
    text = transcribe_audio(TEMP_WAV)
    print(">> 認識結果:", text)

    final_text = text
    stop_flag = True  # ← これで main ループを終了させる
    audio_buffer = []

# -----------------------------
# マイクループ
# -----------------------------
def audio_loop():
    global recording, audio_buffer, stop_flag

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("🎤 Rキー長押しで録音開始 → 離すと停止＆文字起こし")

    try:
        while not stop_flag:
            if recording:
                data = stream.read(CHUNK)
                with lock:
                    audio_buffer.append(data)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

# -----------------------------
# Rキーで録音ON/OFF
# -----------------------------
def toggle_record(event):
    global recording, audio_buffer

    recording = not recording
    if recording:
        print("🎙️ 録音開始")
        audio_buffer = []
    else:
        print("🛑 録音停止 → 変換中...")
        process_buffer()

# -----------------------------
# 外部呼び出し用
# -----------------------------
def start_voice_read():
    global final_text

    # 音声ループを別スレッドで開始
    t = threading.Thread(target=audio_loop, daemon=True)
    t.start()

    # Rキーを登録
    keyboard.on_press_key("r", toggle_record)

    # テキストが取れるまで待つ
    while final_text is None:
        time.sleep(0.1)

    return final_text


# -----------------------------
# デバッグ用
# -----------------------------
if __name__ == "__main__":
    text = start_voice_read()
    print("\n=== 完了 ===")
    print("返されたテキスト:", text)
