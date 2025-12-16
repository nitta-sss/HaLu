#from data.Emotional.Delivary import get_emotion_values
from django.shortcuts import render
from data.emotion_inference import suiron_test


text = "雨降って萎えた"

result = suiron_test(text)

def index(request):

    # text = "怒りで震えてる！許せない！！"
    # a, b = get_emotion_values(text)
    # print(a,b)
    pleasure = result["valence"]
    awakening = result["arousal"]

    # # 念のため float にする
    # pleasure = float(valence)
    # awakening = float(arousal)
    # pleasure = 1
    # awakening = -0.5
    
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
