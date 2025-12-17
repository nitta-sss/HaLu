let bgmEnabled = false; // ★ 初期状態：BGMは有効
const bgm = document.getElementById("BGMsound");
const soundBtn = document.getElementById("soundbtn");

/* ===== 初期BGM再生 ===== */
window.addEventListener("DOMContentLoaded", () => {
    bgm.volume = 0.5; // 音量調整（0.0〜1.0）
    bgm.play().catch(err => {
        console.log("自動再生がブロックされました", err);
    });
});

/* ===== ボタンクリック処理 ===== */
soundBtn.addEventListener("click", () => {

    
    // ▶ BGMを有効化
    if (!bgmEnabled) {
        bgm.volume = 0.5;   // 音量調整
        bgm.play().catch(err => {
            console.log("再生に失敗", err);
        });

        bgmEnabled = true;
        soundBtn.textContent = "BGMを無効化";
        alert("BGMを有効化しました");

    // ▶ BGMを無効化
    } else {
        bgm.pause();
        bgm.currentTime = 0;

        bgmEnabled = false;
        soundBtn.textContent = "音声を有効化";
        alert("BGMを無効化しました");
    }
});