import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time
from datetime import datetime


recording = False
audio_buffer = []
stop_flag = False
final_text = None
lock = threading.Lock()
model = None
# -----------------------------
# 設定
# -----------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
TEMP_WAV = "temp.wav"

# Whisperモデル
def get_model():
    global model
    
    try:
        from faster_whisper import WhisperModel
        print("✅ WhisperModel import 成功")
    except Exception as e:
        print("❌ WhisperModel import 失敗")
        print(type(e), e)

    if model is None:
        print("🔄 Whisperモデル初期化中...")
        model = WhisperModel("small", device="cpu", compute_type="int8")
        print("✅ Whisperモデル初期化完了")
    return model


# -----------------------------
# 音声認識
# -----------------------------
def transcribe_audio(path):
    
    model = get_model()
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


    # ★ 音量正規化（重要）
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val


    # WAV保存
    sf.write(TEMP_WAV, data, SAMPLE_RATE)

    print("⏳ Whisper変換中...")
    text = transcribe_audio(TEMP_WAV)

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
        print("🎤 Rキーで録音 → 停止＆変換")
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
    import keyboard

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
