document.addEventListener("DOMContentLoaded", function () {

    const awakeBar = document.getElementById("awakeBar");
    const pleasureBar = document.getElementById("pleasureBar");

    const emotion = {
        x: Number("{{ awakening }}"),
        y: Number("{{ pleasure }}")
    };

    function normalize(v) {
        return Math.max(0, Math.min(100, (v + 1) * 50));
    }

    function updateGauge() {
        awakeBar.style.width = normalize(emotion.x) + "%";
        pleasureBar.style.width = normalize(emotion.y) + "%";
    }

    //テスト用

    // let emotion = {
    //     x: 0.2,    // 覚醒度：-1 ～ +1
    //     y: -0.5    // 快楽度：-1 ～ +1
    // };
    // function updateGauge() {
    //     awakeBar.style.width = emotion.x + "%";
    //     pleasureBar.style.width = emotion.y + "%";
    //     updateGaugeColors(emotion.x, emotion.y);
    // }

    // updateGauge();

    // setInterval(function () {
    //     emotion.x = Math.floor(Math.random() * 101);
    //     emotion.y = Math.floor(Math.random() * 101);
    //     updateGauge();
    // }, 3000);

    /* ★ 色変化の関数 ★ */
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

});  
