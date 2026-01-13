

window.voiceUI = {

    // SE 定義 
    startSE: new Audio("/static/sound/seOn.mp3"),
    endSE: new Audio("/static/sound/seOff.mp3"),

    start() {
        const btn = document.getElementById("voiceBtn");
        if (!btn) return;

        btn.classList.remove("recording-end");
        btn.classList.add("recording");

        this.startSE.currentTime = 0;
        this.startSE.play().catch(() => {});
    },

    stop() {
        const btn = document.getElementById("voiceBtn");
        if (!btn) return;

        btn.classList.remove("recording");
        btn.classList.add("recording-end");

        this.endSE.currentTime = 0;
        this.endSE.play().catch(() => {});

        setTimeout(() => {
            btn.classList.remove("recording-end");
        }, 1750);
    }
};

// -------------------------
// マイクチェック
// -------------------------
async function checkMicrophone() {
    if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("このブラウザは音声入力に対応していません");
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(t => t.stop());
}

// -------------------------
// エラー表示
// -------------------------
function showError(message) {
    alert(message);
}

// -------------------------
// 録音状態（唯一の真実）
// -------------------------
let isRecording = false;
let isCheckingMic = false;
// -------------------------
// ボタン制御
// -------------------------
document.getElementById("voiceBtn").addEventListener("click", async () => {

    // マイク確認中は何もしない
    if (isCheckingMic) return;

    // ▶ 録音開始
    if (!isRecording) {
        isCheckingMic = true;   // ★ ロックON

        try {
            await checkMicrophone();

            isRecording = true;
            window.voiceUI.start();

        } catch (e) {
            showError(e.message);
        } finally {
            isCheckingMic = false; // ★ 必ず解除
        }
    }

    // ■ 録音停止
    else {
        isRecording = false;
        window.voiceUI.stop();
    }
});

