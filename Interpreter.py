from flask import Flask, jsonify
from YOBIDASI import run_ai

app = Flask(__name__)

@app.route("/ai/run", methods=["POST"])
def ai_run():
    print("📩 /ai/run が呼ばれた")
    result = run_ai()
    print("📤 run_ai 完了、結果を返す")
    return jsonify(result)

if __name__ == "__main__":
    print("🚀 Flask 起動中...")
    app.run(port=5000, debug=True)
