from data.emotion_inference import suiron_test
from Audio.Voice_Read import start_voice_read
from Ollama_Response import llm_generate   

# 音声 → テキスト
text = start_voice_read()

# 人の感情推論
result = suiron_test(text)

# AIの返答生成
ai_reply = llm_generate(text)

# 表示
print("Text:", text)
print("快楽度:", result["valence"])
print("覚醒度:", result["arousal"])
print("感情カテゴリ:", result["category"])
print("セリフ:", result["message"])

print("-----")
print("AIの返答:", ai_reply)
