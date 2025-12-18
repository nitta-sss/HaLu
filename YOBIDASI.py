from data.emotion_inference import suiron_test
from Ollama_Response import llm_generate
from Audio.Voice_Read import get_result

def run_ai():
    print("🤖 run_ai 呼び出し")

    text = get_result()
    if not text:
        return {"error": "音声テキストがありません"}

    result = suiron_test(text)
    reply = llm_generate(text)

    print("Text:", text)
    print("valence:", result["valence"])
    print("arousal:", result["arousal"])
    print("category:", result["category"])
    print("AI:", reply)

    return {
        "text": text,
        "valence": result["valence"],
        "arousal": result["arousal"],
        "category": result["category"],
        "reply": reply
    }
