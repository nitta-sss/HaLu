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

            await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
            await new Promise(r => setTimeout(r, 300));
            await fetch("http://127.0.0.1:5000/ai/run", { method: "POST" })
                .then(res => res.json())
                .then(data => {

                    console.log("AI結果:", data);

                    // ===== 左の会話欄更新 =====
                    addMessage("user", data.text);     // Whisper文字起こし
                    addMessage("bot", data.reply);     // LLM返答

                    // ===== 感情ゲージ更新 =====
                    window.emotion.x = parseFloat(data.arousal); // 覚醒
                    window.emotion.y = parseFloat(data.valence); // 快楽

                    if (typeof updateGauge === "function") {
                        updateGauge();
                    }
                });
        }
    });
});


function addMessage(sender, text) {
    console.log("addMessage 呼ばれた:", sender, text);

    const chatBox = document.querySelector(".chat-box"); //div class chat-boxを参照
    if (!chatBox) return; //chatBoxがnullの場合終了(安全装置)

    const div = document.createElement("div");//divclass作成
    div.className = `balloon ${sender}`;  // balloon→吹き出しのcss
    div.textContent = text;
    chatBox.appendChild(div);//htmlの

    chatBox.scrollTop = chatBox.scrollHeight;
}



