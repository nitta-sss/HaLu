import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
INSERT INTO TestData (発言者ID, テキストデータ, 感情ID, valence, arousal)
               
-- 🌤 弱ポジ・日常（joy / happy）
SELECT 1, '今日は空が明るくて、気が楽だ', 1, 0.4, 0.2 UNION ALL
SELECT 1, '外が気持ちよくて、やる気が出てきた', 2, 0.5, 0.3 UNION ALL
SELECT 1, 'なんか調子がよく、落ち着いてる', 1, 0.4, -0.1 UNION ALL
SELECT 1, '朝から気分が悪くない。この調子で頑張ろう', 1, 0.3, 0.1 UNION ALL
SELECT 1, '今日は案外、気持ちが落ち着いている', 1, 0.3, -0.2 UNION ALL

SELECT 1, 'いい天気だったから、気分が少し晴れた', 1, 0.4, 0.2 UNION ALL
SELECT 1, '景色を見ていたら、自然と気持ちが和らいだ', 1, 0.4, -0.3 UNION ALL
SELECT 1, '時間の流れがゆっくりで、ゆったりしている', 1, 0.3, -0.3 UNION ALL
SELECT 1, '今日は無理せず、落ち着いていこう', 1, 0.3, -0.2 UNION ALL
SELECT 1, '朝少し余裕があって、心が軽い', 2, 0.4, -0.1 UNION ALL

-- 😟 弱ネガ・疲れ（sad）
SELECT 1, '少し疲れが溜まってきて体がだるい', 4, -0.4, -0.2 UNION ALL
SELECT 1, '体が重く、動くのがめんどくさい', 4, -0.4, -0.3 UNION ALL
SELECT 1, '気が乗らず、静かにしていたい', 4, -0.4, -0.4 UNION ALL
SELECT 1, 'やる気が出なくて、集中できない', 4, -0.5, -0.3 UNION ALL
SELECT 1, 'なんとなく調子が出ない', 4, -0.4, -0.2 UNION ALL

SELECT 1, '疲れが取れず、ぼんやりする', 4, -0.4, -0.4 UNION ALL
SELECT 1, '頭がだるくて、すっきりしない', 4, -0.4, -0.3 UNION ALL
SELECT 1, '気分が落ち込み気味で、元気がない', 4, -0.5, -0.4 UNION ALL
SELECT 1, '少し気力が落ちてだるい', 4, -0.4, -0.3 UNION ALL
SELECT 1, 'なにもやる気が起きない', 4, -0.3, -0.4 UNION ALL

-- 😠 怒り・苛立ち（anger）
SELECT 1, '些細なことで気持ちが乱れる', 3, -0.4, 0.4 UNION ALL
SELECT 1, '思うように事が進まず、イライラする', 3, -0.5, 0.4 UNION ALL
SELECT 1, '余裕がなく、気が張ってる', 3, -0.6, 0.5 UNION ALL
SELECT 1, '少しのことでも腹が立つ', 3, -0.4, 0.3 UNION ALL
SELECT 1, '気が荒れてる', 3, -0.5, 0.4 UNION ALL

SELECT 1, 'なんか引っかかって、落ち着かない', 3, -0.5, 0.4 UNION ALL
SELECT 1, '気持ちを切り替えれない', 3, -0.5, 0.4 UNION ALL
SELECT 1, '少しのことでもイライラしそう', 3, -0.4, 0.3 UNION ALL
SELECT 1, '気にしなくていいことで腹を立てる', 3, -0.5, 0.5 UNION ALL
SELECT 1, '心がざわつく', 3, -0.5, 0.4 UNION ALL

-- 😰 不安・心配（worry）
SELECT 1, 'このままでいいのか、不安になる', 6, -0.5, 0.3 UNION ALL
SELECT 1, 'この後のことを考えて気持ちが落ち着かない', 6, -0.6, 0.4 UNION ALL
SELECT 1, 'なんか心配になってきた', 6, -0.5, 0.4 UNION ALL
SELECT 1, '安心できず、そわそわする', 6, -0.6, 0.5 UNION ALL
SELECT 1, '不安でしかない', 6, -0.5, 0.3 UNION ALL

SELECT 1, '先行きが見えず、気が乗らない', 6, -0.6, 0.4 UNION ALL
SELECT 1, '考えすぎて、落ち着かない', 6, -0.6, 0.5 UNION ALL
SELECT 1, '心配してしまって集中できない', 6, -0.6, 0.5 UNION ALL
SELECT 1, '精神的に不安定だ', 6, -0.5, 0.4 UNION ALL
SELECT 1, '不安が残って落ち着けない', 6, -0.5, 0.4 UNION ALL

-- 🌙 落ち着き・回復（joy）
SELECT 1, '少しずつ心が落ち着いてきた', 1, 0.3, -0.4 UNION ALL
SELECT 1, '深呼吸して、落ち着きを取り戻した', 1, 0.3, -0.5 UNION ALL
SELECT 1, '静かにすごすと、気持ちが安定する', 1, 0.4, -0.5 UNION ALL
SELECT 1, '今は調子が悪いから1度休憩しよう', 1, 0.2, -0.5 UNION ALL
SELECT 1, '本でも読んで落ち着きたい', 1, 0.2, -0.4;

""")




conn.commit()

conn.close()
