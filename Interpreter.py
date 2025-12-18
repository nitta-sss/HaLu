from flask import Flask, jsonify
from YOBIDASI import run_ai
from Audio.Voice_Read import start_recording, stop_recording, get_result

app = Flask(__name__)


@app.route("/mic/start", methods=["POST"])
def mic_start():
    start_recording()
    return jsonify({"status": "recording"})

@app.route("/mic/stop", methods=["POST"])
def mic_stop():
    stop_recording()
    return jsonify({"status": "processing"})

@app.route("/ai/run", methods=["POST"])
def ai_run():
    return jsonify(run_ai())
    
if __name__ == "__main__":
    print("🚀 Flask 起動中...")
    app.run(port=5000, debug=True)
