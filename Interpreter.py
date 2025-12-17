from flask import Flask, jsonify
from YOBIDASI import run_ai

app = Flask(__name__)

@app.route("/ai/run", methods=["POST"])
def ai_run():
    print("📩 /ai/run が呼ばれた")
    result = run_ai()
    print("📤 run_ai 完了、結果を返す")
    return jsonify(result)

@app.route("/mic/start", methods=["POST"])
def mic_start():
    start_recording()
    return jsonify({"status": "recording"})

@app.route("/mic/stop", methods=["POST"])
def mic_stop():
    stop_recording()
    return jsonify({
        "status": "done",
        "text": get_result()
    })
    
if __name__ == "__main__":
    print("🚀 Flask 起動中...")
    app.run(port=5000, debug=True)
