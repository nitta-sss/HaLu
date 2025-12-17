from data.emotion_inference import suiron_test
from Audio.Voice_Read import start_voice_read
from Ollama_Response import llm_generate

text = start_voice_read()

result = suiron_test(text)

ai_reply = llm_generate(text)

print("Text:",text)
print("快楽度:", result["valence"])
print("覚醒度:", result["arousal"])
print("感情カテゴリ:", result["category"])
print("------------------------")
print("AIの返答:", ai_reply)
