from emotion_inference import suiron_test

text = "今日は天気がいいので気分がいいです"

result = suiron_test(text)

print("快楽度:", result["valence"])
print("覚醒度:", result["arousal"])
print("感情カテゴリ:", result["category"])
print("セリフ:", result["message"])
