#from data.Emotional.Delivary import get_emotion_values
from django.shortcuts import render
from data.emotion_inference import suiron_test


text = "今日は天気がいいので気分がいいです"

result = suiron_test(text)

def index(request):

    # text = "怒りで震えてる！許せない！！"
    # a, b = get_emotion_values(text)
    # print(a,b)
    valence = result.get("valence", 0)
    arousal = result.get("arousal", 0)

    # 念のため float にする
    pleasure = float(valence)
    awakening = float(arousal)
    # pleasure = 10
    # awakening = 50
    
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
