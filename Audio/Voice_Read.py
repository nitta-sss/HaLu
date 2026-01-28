import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time

recording = False
audio_buffer = []
stop_flag = False
final_text = None
lock = threading.Lock()
model = None

SAMPLE_RATE = 16000
CHANNELS = 1
TEMP_WAV = "temp.wav"

def get_model():
    global model
    from faster_whisper import WhisperModel
    if model is None:
        print("🔄 Whisper 初期化")
        model = WhisperModel("small", device="cpu", compute_type="int8")
    return model

def transcribe_audio(path):
    model = get_model()
    segments, _ = model.transcribe(path, language="ja")
    return "".join(seg.text for seg in segments)

def process_buffer():
    global final_text, stop_flag
    if not audio_buffer:
        return

    data = np.concatenate(audio_buffer, axis=0)
    if np.max(np.abs(data)) > 0:
        data = data / np.max(np.abs(data))

    sf.write(TEMP_WAV, data, SAMPLE_RATE)
    final_text = transcribe_audio(TEMP_WAV)
    print("📝 text:", final_text)
    stop_flag = True

def callback(indata, frames, time_info, status):
    if recording:
        with lock:
            audio_buffer.append(indata.copy())

def audio_loop():
    with sd.InputStream(
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        callback=callback
    ):
        while not stop_flag:
            time.sleep(0.05)

def start_recording():
    global recording, audio_buffer, stop_flag, final_text
    print("🎙️ 録音開始")
    audio_buffer = []
    final_text = None
    stop_flag = False
    recording = True
    threading.Thread(target=audio_loop, daemon=True).start()

def stop_recording():
    global recording
    print("🛑 録音停止")
    recording = False
    process_buffer()

def get_result():
    print("get_result呼び出し：",final_text)
    return final_text

def get_result_Hz():
    print("get_result呼び出し：",final_text)
    y = np.concatenate(audio_buffer, axis=0).reshape(-1).astype(np.float32)
    return final_text,y
