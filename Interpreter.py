from flask import Flask, jsonify, request,Response
from flask_cors import CORS
from Audio.Voice_Read import start_recording, stop_recording, get_result
from YOBIDASI import run_ai, speak_ai, run_ai_voice
from Ollama_Response import reset_conversation
from user_find import set_active_user
from Audio.tone_retake import reload_Hz
from Audio.user_registration import registration_new

import subprocess
import os
import sys
import threading
import traceback
import queue




app = Flask(__name__)
CORS(app)
CURRENT_THEME_ID = "forest"


log_queue = queue.Queue()
#print文をjsに送る
class TeeStdout:
    def __init__(self, original):
        self.original = original

    def write(self, msg):
        # VSCode / ターミナルに表示
        self.original.write(msg)
        self.original.flush()

        # UI用に横取り
        if msg.strip():
            log_queue.put(msg.strip())

    def flush(self):
        self.original.flush()

# stdout / stderr 両方ミラー
sys.stdout = TeeStdout(sys.stdout)
sys.stderr = TeeStdout(sys.stderr)



# ===== CORS 強制許可 =====
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

print("🐍 Flask Python:", sys.executable)

# -------------------------
# しゃべり連打防止（任意）
# -------------------------
_speaking_lock = threading.Lock()
_is_speaking = False

def _safe_json(payload, status=200):
    """必ずJSONで返す"""
    return jsonify(payload), status

@app.route("/mic/start", methods=["POST", "OPTIONS"])
def mic_start():
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        start_recording()
        return _safe_json({"status": "recording"})
    except Exception as e:
        print("❌ mic/start error:", e)
        traceback.print_exc()
        return _safe_json({"error": "MIC_START_FAILED"}, 500)

@app.route("/mic/stop", methods=["POST", "OPTIONS"])
def mic_stop():
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        stop_recording()
        text = get_result()
        print("🎤 flask mic_stop text:", text)
        return _safe_json({"status": "processing", "text": text or ""})
    except Exception as e:
        print("❌ mic/stop error:", e)
        traceback.print_exc()
        return _safe_json({"error": "MIC_STOP_FAILED", "text": ""}, 500)



@app.route("/ai/run", methods=["POST", "OPTIONS"])
def ai_run():
    if request.method == "OPTIONS":
        return ("", 204)

    try:
        # JSから来る: { "text": "..." }
        data = request.get_json(silent=True) or {}
        text = data.get("text", None)

        print("🚀 ai_run called. text:", repr(text))

        # run_ai(text) は dict を返す想定（あなたの既存仕様）
        result = run_ai(text)

        # 保険：dictじゃない場合でも落ちないようにする
        if not isinstance(result, dict):
            result = {"reply": str(result)}

        # 必須キーが無いとJSが困る場合があるので補完（任意）
        result.setdefault("reply", "")
        result.setdefault("valence", None)
        result.setdefault("arousal", None)

        return _safe_json(result)

    except Exception as e:
        print("❌ ai/run error:", e)
        traceback.print_exc()
        return _safe_json({"error": "AI_RUN_FAILED", "reply": ""}, 500)


@app.route("/ai/run_voice", methods=["POST", "OPTIONS"])
def ai_run_voice():
    if request.method == "OPTIONS":
        return ("", 204)

    try:
        # JSから来る: { "text": "..." }
        data = request.get_json(silent=True) or {}
        text = data.get("text", None)

        print("🚀 ai_run called. text:", repr(text))

        # run_ai(text) は dict を返す想定（あなたの既存仕様）
        result = run_ai_voice(text)

        # 保険：dictじゃない場合でも落ちないようにする
        if not isinstance(result, dict):
            result = {"reply": str(result)}

        # 必須キーが無いとJSが困る場合があるので補完（任意）
        result.setdefault("reply", "")
        result.setdefault("valence", None)
        result.setdefault("arousal", None)

        return _safe_json(result)

    except Exception as e:
        print("❌ ai/run_voice error:", e)
        traceback.print_exc()
        return _safe_json({"error": "AI_RUN_FAILED", "reply": ""}, 500)


@app.route("/ai/speak", methods=["POST", "OPTIONS"])
def ai_speak():
    if request.method == "OPTIONS":
        return ("", 204)

    global _is_speaking
    global CURRENT_THEME_ID  # ★追加

    try:
        # ★追加：themeId を受け取る（無い/壊れてても落ちない）
        data = request.get_json(silent=True) or {}
        theme_id = data.get("themeId") or "forest"
        CURRENT_THEME_ID = theme_id
        print("🎭 themeId =", CURRENT_THEME_ID)

        # 連打防止（任意）
        with _speaking_lock:
            if _is_speaking:
                return _safe_json({"status": "busy"})
            _is_speaking = True

        def _worker():
            global _is_speaking
            try:
                print("🗣 speak_ai start")
                speak_ai(CURRENT_THEME_ID)  # ★ここは壊さない（そのまま）
            except Exception as e:
                print("❌ speak_ai error:", e)
                traceback.print_exc()
            finally:
                with _speaking_lock:
                    _is_speaking = False
                print("🗣 speak_ai end")

        threading.Thread(target=_worker, daemon=True).start()
        return _safe_json({"status": "started", "themeId": CURRENT_THEME_ID})  # ★おまけ

    except Exception as e:
        print("❌ ai/speak error:", e)
        traceback.print_exc()
        # lock解除
        with _speaking_lock:
            _is_speaking = False
        return _safe_json({"error": "AI_SPEAK_FAILED"}, 500)


@app.route("/labeler/open", methods=["POST", "OPTIONS"])
def open_labeler():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()

    script = os.path.join(os.path.dirname(__file__), "DB_INSERT_TK.py")

    # Windowsで確実に venv の python で起動
    subprocess.Popen([sys.executable, script, text])

    return jsonify({"status": "opened"})


@app.route("/ai/reset", methods=["POST", "OPTIONS"])
def ai_reset():
    if request.method == "OPTIONS":
        return ("", 204)

    reset_conversation()
    print("🧹 会話履歴をリセットしました")
    return jsonify({"status": "ok"})




@app.route("/ai/tone", methods=["POST", "OPTIONS"])
def user_find():

    # プリフライトは即終了（これで2回ログ問題もスッキリ）
    if request.method == "OPTIONS":
        return ("", 204)

    print("ユーザー選択flsk")

    data = request.get_json(silent=True) or {}
    user = (data.get("activeUser") or "").strip()
    #userHz = (data.get("activeUserHz") or "").strip()

    print("flsk受信JSON:", data)
    print("flskユーザー:", user)
    #print("flskユーザーHz:", userHz)

    if not user:
        return jsonify({"status": "ng", "reason": "activeUser is empty"}), 400

    set_active_user(user)
    return jsonify({"status": "ok"})


@app.route("/ai/tone_retake", methods=["POST", "OPTIONS"])
def Hz_reload():

    # プリフライトは即終了（これで2回ログ問題もスッキリ）
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    user = (data.get("user") or "").strip()
    #userHz = (data.get("activeUserHz") or "").strip()

    print("flsk受信JSON:", data)
    print("flskユーザー:", user)
    
    reload_Hz(user)

    if not user:
        return jsonify({"status": "ng", "reason": "activeUser is empty"}), 400
    return jsonify({"status": "ok"})


@app.route("/ai/tone_newuser", methods=["POST", "OPTIONS"])
def registration():

    # プリフライトは即終了（これで2回ログ問題もスッキリ）
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    user = (data.get("user") or "").strip()
    print("flsk新規登録ユーザー:", user)
    
    registration_new(user)

    if not user:
        return jsonify({"status": "ng", "reason": "activeUser is empty"}), 400
    return jsonify({"status": "ok"})


@app.route("/logs")
def stream_logs():
    def generate():
        while True:
            msg = log_queue.get()
            yield f"data: {msg}\n\n"

    return Response(generate(), mimetype="text/event-stream")
    

if __name__ == "__main__":
    print("🚀 Flask 起動中...")
    # debug=True + use_reloader=False はそのままでOK
    app.run(port=5000, debug=True, use_reloader=False)
