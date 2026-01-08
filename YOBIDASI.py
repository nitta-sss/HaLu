from data.emotion_inference import suiron_test
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result
from Audio.forest_paimon import speak

last_reply = None
def run_ai():
    global last_reply
    #voice_readの結果(テキスト)を返す
    print("結果受け取り")
    text = get_result()
    print("yoasobi:",text)
    if not text:
        return {"error": "音声テキストがありません"}

    #AIによる感情推論
    print("感情推論開始")
    result = suiron_test(text)
    print("感情推論できた", result)

    #返答   
    print("LLM呼び出し開始")
    last_reply = llm_generate(text)
    print("LLM返答:", last_reply)

 
    
    return {
        "text": text,
        "valence": result["valence"],
        "arousal": result["arousal"],
        "category": result["category"],
        "reply": last_reply
    }


def speak_ai():
    global last_reply
    print("発話開始")
    print(last_reply)
    speak(last_reply)
    print("発話終了")