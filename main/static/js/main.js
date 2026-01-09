console.log("✅ main.js 読み込まれたよ");


document.addEventListener("DOMContentLoaded", () => {
    const voiceBtn = document.getElementById("voiceBtn");
    if (!voiceBtn) return;

    let isRecording = false;

    voiceBtn.addEventListener("click", async () => {
        if (!isRecording) {
            isRecording = true;
            window.voiceUI.start();

            await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });

        } else {
            isRecording = false;
            window.voiceUI.stop();

            const stopRes = await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
            const stopData = await stopRes.json();

            console.log("mic/stop 結果:", stopData);

            // 2️⃣ 先にユーザーの文字起こしだけ表示
            if (stopData.text) {
                addMessage("user", stopData.text);   // ← final_text がここ
            }

            await new Promise(r => setTimeout(r, 300));
            await fetch("http://127.0.0.1:5000/ai/run", { method: "POST" })
                .then(res => res.json())
                .then(async (data) => {

            console.log("AI結果:", data);

            // ===== 感情ゲージ更新 =====
            window.emotion.x = parseFloat(data.arousal);
            window.emotion.y = parseFloat(data.valence);
            window.updateGauge();

            console.time("AI_FLOW");
            console.timeLog("AI_FLOW", "typing start");
            // ① 空の吹き出し作成
            const botDiv = addMessageElement("bot");

            // ② タイプライター開始（Promise）非同期処理
            const typingPromise = typeWriter(botDiv, data.reply, 25);//作成したdivの中にAI返答を入れる

            console.timeLog("AI_FLOW", "voice fetch start");
            // ③ 読み上げ開始（ここは “待たない”）非同期処理
            fetch("http://127.0.0.1:5000/ai/speak", { method: "POST" });
            
            console.timeLog("AI_FLOW", "typing end");
            console.timeEnd("AI_FLOW");
            // ④ 表示が全部終わるまで待ちたいならこれ（任意）
            await typingPromise;
        });
            
           
            
        }
    });
});

function addMessage(sender, text) {
    console.log("addMessage 呼ばれた:", sender, text);

    const chatBox = document.querySelector(".chat-box");
    if (!chatBox) return;

    const div = document.createElement("div");
    div.className = `balloon ${sender}`; // balloon user / balloon bot
    div.textContent = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function addMessageElement(sender) {
    const chatBox = document.querySelector(".chat-box");//chat-boxに接続
    if (!chatBox) return null;

    const div = document.createElement("div");
    div.className = `balloon ${sender}`;
    div.textContent = ""; // 空で作る
    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function typeWriter(div, fullText, msPerChar = 200) {
    return new Promise(resolve => {
        if (!div) return resolve();

        let i = 0;
        const chatBox = document.querySelector(".chat-box");//自動スクロール

        const timer = setInterval(() => {//25ms秒ごとに1文字追加
            div.textContent += fullText[i];
            i++;

            if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;

            if (i >= fullText.length) {//全ての文字を出力したか判定
                clearInterval(timer);//タイマー停止
                resolve();
            }
        }, msPerChar);
    });
}




