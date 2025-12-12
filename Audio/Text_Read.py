import pyttsx3

def read_text(text):
    # エンジンの初期化
    engine = pyttsx3.init()

    # 速度設定　0に近づくほど遅くなる
    engine.setProperty('rate', 200)  

    # 音量設定　0.0(無音)～1.0(最大音量)
    engine.setProperty('volume', 0.5) 

    # テキストを読み上げる
    engine.say(text)

    # 読み上げを実行
    engine.runAndWait()

if __name__ == "__main__":
    """
    with open('C:/Users/232144/Desktop/HaLu/src/Audio/test.txt',encoding='utf-8') as f:
        print('with通過')
        for line in f:
            print(line)
    """

    read_text("こんにちは")


