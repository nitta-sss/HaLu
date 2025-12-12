import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
INSERT INTO TestData (発言者ID, テキストデータ, 感情ID, valence, arousal)
               
-- 🌤 弱ポジ・日常（joy / happy）
SELECT 1, '天気いいからめっちゃ気分いいわ', 1, 0.4, 0.2 UNION ALL
SELECT 1, '外の風気持ちいから元気出てきた', 2, 0.5, 0.3 UNION ALL
SELECT 1, 'なんとなく調子がよく、リラックスできてる', 1, 0.4, -0.1 UNION ALL
SELECT 1, '今日気分悪くならなくてガチ調子いい', 1, 0.3, 0.1 UNION ALL
SELECT 1, '今日メンタルだいぶ安定してる', 1, 0.3, -0.2 UNION ALL

SELECT 1, '空気きれいすぎて気分いいわ', 1, 0.4, 0.2 UNION ALL
SELECT 1, '空眺めてると、落ち着いてくる', 1, 0.4, -0.3 UNION ALL
SELECT 1, '平和すぎてなかなかいいな', 1, 0.3, -0.3 UNION ALL
SELECT 1, '今日は無理せずゆっくりしてよ', 1, 0.3, -0.2 UNION ALL
SELECT 1, 'ちょっと余裕出来て心楽だわ', 2, 0.4, -0.1 UNION ALL

-- 😟 弱ネガ・疲れ（sad）
SELECT 1, 'ちょっと疲れてきた', 4, -0.4, -0.2 UNION ALL
SELECT 1, '体重すぎて動きたくねえ', 4, -0.4, -0.3 UNION ALL
SELECT 1, '気分乗んないから一人でいたい', 4, -0.4, -0.4 UNION ALL
SELECT 1, 'やる気でないから集中できない', 4, -0.5, -0.3 UNION ALL
SELECT 1, '調子上がんないわ', 4, -0.4, -0.2 UNION ALL

SELECT 1, '疲れた待ってて頭ぼんやりしてきた', 4, -0.4, -0.4 UNION ALL
SELECT 1, '頭重すぎてすっきりしない', 4, -0.4, -0.3 UNION ALL
SELECT 1, '萎えすぎて元気でない', 4, -0.5, -0.4 UNION ALL
SELECT 1, '少し気力が落ちている感じがする', 4, -0.4, -0.3 UNION ALL
SELECT 1, '無理せず楽したい', 4, -0.3, -0.4 UNION ALL

-- 😠 怒り・苛立ち（anger）
SELECT 1, 'ちょっとなんかあると気持ち乱れる', 3, -0.4, 0.4 UNION ALL
SELECT 1, '思い通りにいかなくてちょっとイライラする', 3, -0.5, 0.4 UNION ALL
SELECT 1, '余裕なくて気持ち張りつめてきた', 3, -0.6, 0.5 UNION ALL
SELECT 1, 'ちっちゃいことでも気に障ることあるわ', 3, -0.4, 0.3 UNION ALL
SELECT 1, '気持ち荒れやすい', 3, -0.5, 0.4 UNION ALL

SELECT 1, 'ずっと心残りあって落ち着かない', 3, -0.5, 0.4 UNION ALL
SELECT 1, '感情切り替えムズイ', 3, -0.5, 0.4 UNION ALL
SELECT 1, 'ちょっと神経質気味かも', 3, -0.4, 0.3 UNION ALL
SELECT 1, '余計なことで気が立ってくる', 3, -0.5, 0.5 UNION ALL
SELECT 1, '感情が内側でもやもやしてる', 3, -0.5, 0.4 UNION ALL

-- 😰 不安・心配（worry）
SELECT 1, 'ほんとにこれでいいんかなって不安なる', 6, -0.5, 0.3 UNION ALL
SELECT 1, '先のこと考えてると落ち着かねえ', 6, -0.6, 0.4 UNION ALL
SELECT 1, '心配が浮かんできて不安', 6, -0.5, 0.4 UNION ALL
SELECT 1, '安心できなくて気持ちがざわついてる', 6, -0.6, 0.5 UNION ALL
SELECT 1, 'ずっと不安', 6, -0.5, 0.3 UNION ALL

SELECT 1, '先行きが見えなくて疲れる', 6, -0.6, 0.4 UNION ALL
SELECT 1, '考えすぎで落ち着けない', 6, -0.6, 0.5 UNION ALL
SELECT 1, '心配事が気になって頭回んない', 6, -0.6, 0.5 UNION ALL
SELECT 1, 'マジ不安', 6, -0.5, 0.4 UNION ALL
SELECT 1, '落ち着けないくらい不安', 6, -0.5, 0.4 UNION ALL

-- 🌙 落ち着き・回復（joy）
SELECT 1, 'ちょっと気持ち楽になってきた', 1, 0.3, -0.4 UNION ALL
SELECT 1, '深呼吸したら落ち着いてきた', 1, 0.3, -0.5 UNION ALL
SELECT 1, '一人の時間が気持ち整えてくれる', 1, 0.4, -0.5 UNION ALL
SELECT 1, '無理せず休んどいたほういいかも', 1, 0.2, -0.5 UNION ALL
SELECT 1, '心身ともに疲れてるから休息が必要だわ', 1, 0.2, -0.4;

""")




conn.commit()

conn.close()
