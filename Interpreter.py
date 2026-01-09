from flask import Flask, jsonify, request
from Audio.Voice_Read import start_recording, stop_recording, get_result
from YOBIDASI import run_ai, speak_ai
import sys
import threading


app = Flask(__name__)

# ===== CORS 強制許可 =====
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

print("🐍 Flask Python:", sys.executable)

@app.route("/mic/start", methods=["POST", "OPTIONS"])
def mic_start():
    if request.method == "OPTIONS":
        return ("", 204)
    start_recording()
    return jsonify({"status": "recording"})

@app.route("/mic/stop", methods=["POST", "OPTIONS"])
def mic_stop():
    if request.method == "OPTIONS":
        return ("", 204)
    stop_recording()
    text = get_result()
    print("flask", text)
    return jsonify({"status": "processing", "text": text or ""})

@app.route("/ai/run", methods=["POST", "OPTIONS"])
def ai_run():
    if request.method == "OPTIONS":
        return ("", 204)

    # ★キーボード入力はここで受け取る
    data = request.get_json(silent=True) or {}
    text = data.get("text")  # 無ければ None

    print("🚀 ai_run 呼び出し text:", text)

    # ★textがあればそれを使う / 無ければrun_ai側でget_result()
    return jsonify(run_ai(text))

@app.route("/ai/speak", methods=["POST", "OPTIONS"])
def ai_speak():
    if request.method == "OPTIONS":
        return ("", 204)
    print("🚀 ai_speak 呼び出し")
    threading.Thread(target=speak_ai, daemon=True).start()
    return jsonify({"status": "started"})

if __name__ == "__main__":
    print("🚀 Flask 起動中...")
    app.run(port=5000, debug=True)
