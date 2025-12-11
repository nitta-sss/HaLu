import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import keyboard
import time
from faster_whisper import WhisperModel
from datetime import datetime

recording = False
audio_buffer = []
stop_flag = False
final_text = None
lock = threading.Lock()

# -----------------------------
# 設定
# -----------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
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
# バッファ → WAV → Whisper
# -----------------------------
def process_buffer():
    global audio_buffer, final_text, stop_flag

    if not audio_buffer:
        return

    print("🛠 WAV生成中...")

    # numpy 配列にまとめる
    data = np.concatenate(audio_buffer, axis=0)

    # WAV保存
    sf.write(TEMP_WAV, data, SAMPLE_RATE)

    print("⏳ Whisper変換中...")
    text = transcribe_audio(TEMP_WAV)

    print(">> 認識結果:", text)

    final_text = text
    stop_flag = True


# -----------------------------
# 録音コールバック
# -----------------------------
def callback(indata, frames, time_info, status):
    global audio_buffer, recording
    if recording:
        with lock:
            audio_buffer.append(indata.copy())  # numpy形式で保存


# -----------------------------
# 録音スレッド
# -----------------------------
def audio_loop():
    with sd.InputStream(
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            callback=callback):
        print("🎤 Rキー長押しで録音 → 離すと停止＆変換")
        while not stop_flag:
            time.sleep(0.05)


# -----------------------------
# Rキー ON/OFF
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

    # 録音スレッド開始
    t = threading.Thread(target=audio_loop, daemon=True)
    t.start()

    # Rキー動作登録
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
