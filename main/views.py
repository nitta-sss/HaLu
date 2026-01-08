from django.shortcuts import render
from data.emotion_inference import suiron_test
from django.http import JsonResponse
from Ollama_Response import reset_conversation
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):

    # 仮の入力（あとでPOSTや音声認識に置き換える）
    text = "おこっています"

    result = suiron_test(text)

    pleasure = float(result["valence"])
    awakening = float(result["arousal"])

    messages = [
        {"sender": "bot",  "text": "おいらは森のパイモン。気軽に話しかけてね"},
    ]

    return render(request, "index.html", {
        "awakening": awakening,
        "pleasure": pleasure,
        "messages": messages,
    })

def run_python_view(request):
    if request.method == "POST":
        reset_conversation()   # ← ここで実行される
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)