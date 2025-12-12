
import sys
sys.path.append("C:/Users/232144/Desktop/HaLu_venv/HALU/Audio/")#ここはファイルパス。自分のに変換して
sys.path.append("C:/Users/232144/Desktop/HaLu_venv/HALU/")

import Voice_Read
print("Voice_Read import OK")

import Emotional_Reasoning
print("Emotional_Reasoning import OK")


text = Voice_Read.start_voice_read()#音声認識機能起動
val, aro=Emotional_Reasoning.suiron_test(text)#感情予測機能起動

print("音声認識：",text)
print(f"快ー不快: {val}\n覚醒ー静寂: {aro}")


