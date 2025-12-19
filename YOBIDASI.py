from data.emotion_inference import suiron_test
from Audio.Voice_Read import start_recording
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result
from Audio.forest_paimon import speak

def run_ai():
    #voice_readの結果(テキスト)を返す
    print("結果受け取り")
    text = get_result()
    print("yoasobi:",text)
    if not text:
        return {"error": "音声テキストがありません"}

    #AIによる感情推論
    result = suiron_test(text)
    #返答
    ai_reply = llm_generate(text)
    speak(ai_reply)
    return {
        "text": text,
        "valence": result["valence"],
        "arousal": result["arousal"],
        "category": result["category"],
        "reply": ai_reply
    }