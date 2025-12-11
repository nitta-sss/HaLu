#from data.Emotional.Delivary import get_emotion_values
from django.shortcuts import render

def index(request):

    # text = "怒りで震えてる！許せない！！"
    # a, b = get_emotion_values(text)
    # print(a,b)
    pleasure = 100
    awakening = 100

    messages = [
        {"sender": "user", "text": "こんにちは！"},
        {"sender": "bot",  "text": "リラックスしてるよ"},
        {"sender": "user", "text": "今日は調子いい？"},
        {"sender": "bot",  "text": "だまれ"},
        {"sender": "bot",  "text": "だまれ"},
        {"sender": "bot",  "text": "だまれだまれだまれだまれだまれだまれ"},
        {"sender": "bot",  "text": "だまれ"},
        {"sender": "user", "text": "こんにちは！"},
        {"sender": "bot",  "text": "リラックスしてるよ"},
        {"sender": "user", "text": "今日は調子いい？"},
        {"sender": "bot",  "text": "だまれ"},
        {"sender": "bot",  "text": "だまれ"},
        {"sender": "bot",  "text": "だまれだまれだまれだまれだまれだまれ"},
        {"sender": "bot",  "text": "だまれ"},
    ]


    return render(request, "index.html", {
        "awakening": awakening,
        "pleasure": pleasure,
        "messages": messages,
    })
