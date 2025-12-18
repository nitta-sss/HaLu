from data.emotion_inference import suiron_test
from Audio.Voice_Read import start_recording
from Ollama_Response import llm_generate
from Audio.zunda import speak_now

# 音声からテキスト
text = start_recording()

# 感情推論
result = suiron_test(text)

# AI返答生成
ai_reply = llm_generate(text)

print("Text:",text)
print("快楽度:", result["valence"])
print("覚醒度:", result["arousal"])
print("感情カテゴリ:", result["category"])
print("------------------------")
speak_now(ai_reply)
print("AIの返答:", ai_reply)


