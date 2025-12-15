
import sys

sys.path.append("C:/Users/232144/Desktop/HaLu_venv/HALU/Audio/")#ここはファイルパス。自分のに変換して
sys.path.append("C:/Users/232144/Desktop/HaLu_venv/HALU/data/")
sys.path.append("C:/Users/232144/Desktop/HaLu_venv/HALU/Audio/")

"""
sys.path.append("C:/Users/snitt/Desktop/HALU_venv/HaLu/Audio/")#ここはファイルパス。自分のに変換して
sys.path.append("C:/Users/snitt/Desktop/HaLu_venv/HALU/data/")
sys.path.append("C:/Users/snitt/Desktop/HaLu_venv/HALU/Audio/")
"""
#sys.path.append("C:/Users/232116/Desktop/New_HaLu/HALU/Audio/")#たけとPCpath
#sys.path.append("C:/Users/232116/Desktop/New_HaLu/HALU/")


import Voice_Read
print("Voice_Read import OK")

import ModelTest_sora
print("Emotional_Reasoning import OK")

import Text_Read
print("Text_Read import OK")

Text_Read.read_text("ライブラリimport完了")

Text_Read.read_text("音声認識システム起動")
Text_Read.read_text("ボタンを押して読み取りを開始します")
text = Voice_Read.start_voice_read()#音声認識機能起動

Text_Read.read_text("テキストを受信")
Text_Read.read_text("感情予測を開始します")
val, aro=ModelTest_sora.suiron_test_kari(text)#感情予測機能起動



print("音声認識：",text)
print(f"快ー不快: {val}\n覚醒ー静寂: {aro}")

return render(request, "index.html", {
    "val":val,
    "aro":aro
})


