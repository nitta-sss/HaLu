from data.emotion_inference import suiron_test
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result
from Audio.forest_paimon import speak
import time
from Audio.tone import analyze_tone

last_reply = None

def run_ai(text=None):
    global last_reply
    print("結果受け取り")

    # ★ text が渡されていればそれを使う（キーボード入力用）
    # ★ text が無ければ今まで通り音声認識結果(get_result)を使う（音声入力用）
    if text is None:
        text = get_result()
        

    print("yoasobi:", text)

    if not text:
        return {"error": "テキストがありません"}

    # AIによる感情推論(user)
    print("感情推論開始")
    result = suiron_test(text)
    print("感情推論できた", result)

    # 返答
    print("LLM呼び出し開始")
    last_reply = llm_generate(text)
    print("LLM返答:", last_reply)

    # AIによる感情推論(Ollamax)
    print("感情推論開始")
    result_ollamax = suiron_test(last_reply)
    print("感情推論できた", result_ollamax)

    return {
        "text": text,
        "valence": result["valence"],
        "arousal": result["arousal"],
        "category": result["category"],
        "reply": last_reply
    }

def speak_ai(type):
    global last_reply
    print("発話開始")
    print(last_reply)
    print("🔊 speak called:", time.time())
    
    # last_reply が None のとき落ちないように保険
    #type="forest"
    speak(last_reply or "",type)
    print("🔊 speak finished:", time.time())
    print("発話終了")

    # Flaskがjsonifyするので辞書返す（フロントが使わなくてもOK）
    return {"status": "ok"}
