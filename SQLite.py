import sqlite3

conn = sqlite3.connect("AI.db")

cursor = conn.cursor()


cursor.execute("""
INSERT INTO TestData (発言者ID, テキストデータ, 感情ID, valence, arousal)

-- 🌤 弱ポジ・日常（joy / happy）
SELECT 1, '今日は空が明るくて、気分も少し軽い', 1, 0.4, 0.2 UNION ALL
SELECT 1, '外が気持ちよくて、前向きな気分になってきた', 2, 0.5, 0.3 UNION ALL
SELECT 1, 'なんとなく調子がよく、落ち着いて過ごせている', 1, 0.4, -0.1 UNION ALL
SELECT 1, '朝から気分が悪くなく、このまま進めそうだ', 1, 0.3, 0.1 UNION ALL
SELECT 1, '今日は比較的、気持ちが安定している', 1, 0.3, -0.2 UNION ALL

SELECT 1, '空気が澄んでいて、気分が少し晴れた', 1, 0.4, 0.2 UNION ALL
SELECT 1, '外を見ていたら、自然と気持ちが和らいだ', 1, 0.4, -0.3 UNION ALL
SELECT 1, '穏やかな時間が流れていて、悪くない気分だ', 1, 0.3, -0.3 UNION ALL
SELECT 1, '今日は無理せず、落ち着いて過ごせそうだ', 1, 0.3, -0.2 UNION ALL
SELECT 1, '少し余裕があって、心が軽い', 2, 0.4, -0.1 UNION ALL

-- 😐 中立（neutral）
SELECT 1, '今日は特に大きな出来事はない', 0, 0.0, 0.0 UNION ALL
SELECT 1, '淡々とした時間を過ごしている', 0, 0.0, -0.2 UNION ALL
SELECT 1, '今のところ、気持ちは可もなく不可もない', 0, 0.0, 0.0 UNION ALL
SELECT 1, '普段通りの流れで一日が進んでいる', 0, 0.0, -0.1 UNION ALL
SELECT 1, '特別な感情は浮かんでいない', 0, 0.0, -0.3 UNION ALL

SELECT 1, 'いつもと変わらない感覚で過ごしている', 0, 0.0, -0.1 UNION ALL
SELECT 1, '今は特に意識する感情がない', 0, 0.0, -0.2 UNION ALL
SELECT 1, '静かに時間が過ぎているだけだ', 0, 0.0, -0.3 UNION ALL
SELECT 1, '感情の波はほとんどない状態だ', 0, 0.0, -0.2 UNION ALL
SELECT 1, '大きな気分の変化は感じていない', 0, 0.0, 0.0 UNION ALL

-- 😟 弱ネガ・疲れ（sad）
SELECT 1, '少し疲れが溜まってきた気がする', 4, -0.4, -0.2 UNION ALL
SELECT 1, '体が重く、動くのが少し億劫だ', 4, -0.4, -0.3 UNION ALL
SELECT 1, '気分が乗らず、静かにしていたい', 4, -0.4, -0.4 UNION ALL
SELECT 1, 'やる気が出にくく、集中しづらい', 4, -0.5, -0.3 UNION ALL
SELECT 1, 'なんとなく調子が上がらない', 4, -0.4, -0.2 UNION ALL

SELECT 1, '疲れが抜けず、ぼんやりしている', 4, -0.4, -0.4 UNION ALL
SELECT 1, '頭が重く、すっきりしない', 4, -0.4, -0.3 UNION ALL
SELECT 1, '気分が沈みがちで、元気が出ない', 4, -0.5, -0.4 UNION ALL
SELECT 1, '少し気力が落ちている感じがする', 4, -0.4, -0.3 UNION ALL
SELECT 1, '無理をしたくない気分だ', 4, -0.3, -0.4 UNION ALL

-- 😠 怒り・苛立ち（anger）
SELECT 1, '小さなことで気持ちが乱れてしまった', 3, -0.4, 0.4 UNION ALL
SELECT 1, '思うように進まず、少し苛立っている', 3, -0.5, 0.4 UNION ALL
SELECT 1, '余裕がなく、気持ちが張りつめている', 3, -0.6, 0.5 UNION ALL
SELECT 1, 'ささいなことが気に障ってしまう', 3, -0.4, 0.3 UNION ALL
SELECT 1, '気持ちが荒れやすくなっている', 3, -0.5, 0.4 UNION ALL

SELECT 1, '心に引っかかることがあり、落ち着かない', 3, -0.5, 0.4 UNION ALL
SELECT 1, '感情をうまく切り替えられない', 3, -0.5, 0.4 UNION ALL
SELECT 1, '少し神経質になっている気がする', 3, -0.4, 0.3 UNION ALL
SELECT 1, '余計なことで気が立っている', 3, -0.5, 0.5 UNION ALL
SELECT 1, '感情が内側でざわついている', 3, -0.5, 0.4 UNION ALL

-- 😰 不安・心配（worry）
SELECT 1, 'このままでいいのか、少し不安がある', 6, -0.5, 0.3 UNION ALL
SELECT 1, '先のことを考えると落ち着かない', 6, -0.6, 0.4 UNION ALL
SELECT 1, 'なんとなく心配が頭に浮かんでくる', 6, -0.5, 0.4 UNION ALL
SELECT 1, '安心できず、気持ちがざわついている', 6, -0.6, 0.5 UNION ALL
SELECT 1, '不安が完全には消えない', 6, -0.5, 0.3 UNION ALL

SELECT 1, '先行きが見えず、少し気が重い', 6, -0.6, 0.4 UNION ALL
SELECT 1, '考えすぎて、落ち着きを失っている', 6, -0.6, 0.5 UNION ALL
SELECT 1, '心配事が気になって集中できない', 6, -0.6, 0.5 UNION ALL
SELECT 1, '気持ちが不安定になっている', 6, -0.5, 0.4 UNION ALL
SELECT 1, '落ち着こうとしても不安が残る', 6, -0.5, 0.4 UNION ALL

-- 🌙 落ち着き・回復（joy）
SELECT 1, '少しずつ気持ちが落ち着いてきた', 1, 0.3, -0.4 UNION ALL
SELECT 1, '深呼吸して、心が静まった', 1, 0.3, -0.5 UNION ALL
SELECT 1, '静かな時間が、気持ちを整えてくれる', 1, 0.4, -0.5 UNION ALL
SELECT 1, '今は無理をせず、休むのがよさそうだ', 1, 0.2, -0.5 UNION ALL
SELECT 1, '心身を休めたい気分だ', 1, 0.2, -0.4;

""")




conn.commit()

conn.close()
