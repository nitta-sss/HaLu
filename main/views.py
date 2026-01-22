from django.shortcuts import render
from data.emotion_inference import suiron_test
from django.http import JsonResponse
from django.http import HttpResponse
from Ollama_Response import reset_conversation
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import os


def users_txt(request):
    path = os.path.join(settings.BASE_DIR, "HaLu","users.txt")  # manage.pyと同階層
    if not os.path.exists(path):
        return HttpResponse("not found", status=404, content_type="text/plain")

    with open(path, "r", encoding="utf-8") as f:
        return HttpResponse(f.read(), content_type="text/plain; charset=utf-8")


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