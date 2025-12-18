from django.shortcuts import render
from data.emotion_inference import suiron_test


def index(request):

    # 仮の入力（あとでPOSTや音声認識に置き換える）
    text = "おこっています"

    result = suiron_test(text)

    pleasure = float(result["valence"])
    awakening = float(result["arousal"])

    messages = [
        {"sender": "user", "text": "こんにちは！"},
        {"sender": "bot",  "text": "リラックスしてるよ"},
        {"sender": "user", "text": "今日は調子いい？"},
        {"sender": "bot",  "text": "だまれ"},
    ]

    return render(request, "index.html", {
        "awakening": awakening,
        "pleasure": pleasure,
        "messages": messages,
    })
