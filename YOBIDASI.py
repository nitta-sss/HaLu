from data.emotion_inference import suiron_test
from Audio.Voice_Read import start_voice_read

text = start_voice_read()

result = suiron_test(text)

print("Text:",text)
print("快楽度:", result["valence"])
print("覚醒度:", result["arousal"])
print("感情カテゴリ:", result["category"])
print("--------------------rr-")
print("AIの返答:", ai_reply)
