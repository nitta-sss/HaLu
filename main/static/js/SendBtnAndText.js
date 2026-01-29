
//テキストボックスの中身判定して送信ボタンの色を変える

console.log("✅ SendBtnAndText.js 読み込まれたよ");

document.addEventListener("DOMContentLoaded", () => {
    
    const textInput = document.getElementById("textInput");
    const sendBtn   = document.getElementById("sendBtn");
    //判定
    if (!textInput || !sendBtn) {
        console.warn("❌ textInput or sendBtn not found");
        return;
    }

    //状態更新
    function updateSendBtnState() {
        const hasText = textInput.value.trim() !== "";
        const busy = window.isBusy === true;

        if (hasText && !busy) {
        sendBtn.classList.add("active");
        sendBtn.disabled = false;
        } else {
        sendBtn.classList.remove("active");
        sendBtn.disabled = true;
        }
    }

    // 入力が変わったら状態更新
    textInput.addEventListener("input", updateSendBtnState);

    // 初期状態を反映
    updateSendBtnState();

    // 他ファイルから呼べるように公開
    window.updateSendBtnState = updateSendBtnState;
});