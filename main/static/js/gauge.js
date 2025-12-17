document.addEventListener("DOMContentLoaded", function () {
    const emotion = window.emotion;
    const awakeBar = document.getElementById("awakeBar");
    const pleasureBar = document.getElementById("pleasureBar");
    let prevAwake = null;
    let prevPleasure = null;

    function normalize(v) {
        const percent = (v + 1) * 50;   // -1→0, 0→50, +1→100
        return Math.max(0, Math.min(100, percent)); // 念のため100超えてもいいように制限
    }

    //テスト用

    // let emotion = {
    //     x: 0,    // 覚醒度：-1 ～ +1
    //     y: 0    // 快楽度：-1 ～ +1
    // };

    // ゲージを動かす場所
    function updateGauge() {
        const awakePercent = normalize(emotion.x);
        const pleasurePercent = normalize(emotion.y);
    
        awakeBar.style.width = awakePercent + "%";
        pleasureBar.style.width = pleasurePercent + "%";
    
    // ゲージに色を反映させる
    updateGaugeColors(awakePercent, pleasurePercent);

    if (prevAwake !== null && prevAwake !== awakePercent) {
        playSound();
    }
    if (prevPleasure !== null && prevPleasure !== pleasurePercent) {
        playSound();
    }

    prevAwake = awakePercent;
    prevPleasure = pleasurePercent;
    }

    updateGauge();

    // テスト用ランダムで値を出す
    // setInterval(function () {
    //     // emotion.x = Math.random() * 2 - 1;  // -1 ～ +1
    //     // emotion.y = Math.random() * 2 - 1;  // -1 ～ +1

    //     console.log("emotion raw:", emotion);
    //     console.log("awake %:", normalize(emotion.x));
    //     console.log("pleasure %:", normalize(emotion.y));

    //     updateGauge();
    // }, 3000);

    // 色を値によって変化させる
    function updateGaugeColors(x, y) {

    /* --- 覚醒度：赤→オレンジ→黄 --- */
    let v1 = x / 100;
    let r1 = Math.round(255 * v1);
    let b1 = Math.round(255 * (1 - v1));
    let color1 = `rgb(${r1}, 0, ${b1})`;

    awakeBar.style.background = `linear-gradient(to right, ${color1}, #ffffff60)`;


    /* --- 快楽度（★赤→オレンジ→黄） --- */
    if (y < 30) {
        pleasureBar.style.background = "linear-gradient(to right, red, orange)";
    } else if (y < 70) {
        pleasureBar.style.background = "linear-gradient(to right, orange, yellow)";
    } else {
        pleasureBar.style.background = "linear-gradient(to right, yellow, lightyellow)";
    }
}
/* ▼▼ ゲージ表示/非表示ボタン ▼▼ */
const btn = document.getElementById("showbtn");
const gauge = document.getElementById("emotionArea");


btn.addEventListener("click", function () {
    gauge.classList.toggle("hide");
    btn.textContent = gauge.classList.contains("hide") ? "ゲージ表示" : "ゲージ非表示";
});

function playSound() {
    if (!soundEnabled) return;   // ← ★ 無効なら即終了

    sound.currentTime = 0;
    sound.play().catch(err => {
        console.log("再生エラー:", err);
    });
}})