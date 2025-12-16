document.addEventListener("DOMContentLoaded", function () {

    const awakeBar = document.getElementById("awakeBar");
    const pleasureBar = document.getElementById("pleasureBar");

    // 値を受け取るやつ
    const emotion = {
        x: Number("{{ awakening }}"),
        y: Number("{{ pleasure }}")
    };

    // let prevAwake = null;
    // let prevPleasure = null;

    function normalize(v) {
        const percent = (v + 1) * 50;   // -1→0, 0→50, +1→100
        return Math.max(0, Math.min(100, percent)); // 念のため制限
    }

    function updateGauge() {
        awakeBar.style.width = normalize(emotion.x) + "%";
        pleasureBar.style.width = normalize(emotion.y) + "%";
    }

    //テスト用

    // let emotion = {
    //     x: 0,    // 覚醒度：-1 ～ +1
    //     y: 0    // 快楽度：-1 ～ +1
    // };

    // function updateGauge() {
    //     const awakePercent = normalize(emotion.x);
    //     const pleasurePercent = normalize(emotion.y);
    
    //     awakeBar.style.width = awakePercent + "%";
    //     pleasureBar.style.width = pleasurePercent + "%";
    
    //     // ★ 色を反映させる
        // updateGaugeColors(awakePercent, pleasurePercent);
    
        // if (prevAwake !== null && prevAwake !== awakePercent) {
        //     playSound();
        // }
        // if (prevPleasure !== null && prevPleasure !== pleasurePercent) {
        //     playSound();
        // }
    
        // prevAwake = awakePercent;
        // prevPleasure = pleasurePercent;
    // }

    updateGauge();

    // setInterval(function () {
    //     // emotion.x = Math.random() * 2 - 1;  // -1 ～ +1
    //     // emotion.y = Math.random() * 2 - 1;  // -1 ～ +1

    //     console.log("emotion raw:", emotion);
    //     console.log("awake %:", normalize(emotion.x));
    //     console.log("pleasure %:", normalize(emotion.y));

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

    function playSound() {
        if (!soundEnabled) return;   // ← ★ 無効なら即終了
    
        sound.currentTime = 0;
        sound.play().catch(err => {
            console.log("再生エラー:", err);
        });
    }

    let soundEnabled = false;
    const sound = document.getElementById("gaugeSound");
    const soundBtn = document.getElementById("soundbtn");

    soundBtn.addEventListener("click", function () {

        // ▶ 音声が「無効」→「有効」にする
        if (!soundEnabled) {
            sound.play().then(() => {
                sound.pause();
                sound.currentTime = 0;

                soundEnabled = true;
                soundBtn.textContent = "🔇 音声を無効化";
                alert("音声を有効化しました");
            }).catch(err => {
                console.log("音声の有効化に失敗", err);
            });

        // ▶ 音声が「有効」→「無効」にする
        } else {
            soundEnabled = false;
            soundBtn.textContent = "🔊 音声を有効化";
            alert("音声を無効化しました");
        }
    });

        // ==== 起動ボタン・動画制御 ====

    const startbtn = document.getElementById("startbtn");
    const startvideo = document.getElementById("startvideo");
    const icon = document.getElementById("icon");
    const startArea = document.querySelector(".start-area"); // ← ★先に取る

    /* 🔄 ページ起動時の初期状態 */
    startArea.style.display = "none";
    startvideo.pause();
    startvideo.currentTime = 0;
    icon.style.display = "none";

    startbtn.textContent = "起動";
    startbtn.disabled = false;

    /* ▶ 起動ボタン */
    startbtn.addEventListener("click", () => {
        console.log("起動ボタンが押されました");

        startbtn.textContent = "起動中";
        startbtn.disabled = true;

        startvideo.style.display = "block"; // ← 明示的に表示
        startvideo.currentTime = 0;
        startvideo.play();
    });

    /* ▶ 動画の進行監視（これが一番安定） */
    startvideo.addEventListener("timeupdate", () => {
        if (startvideo.currentTime >= startvideo.duration - 0.1) {
            console.log("動画を非表示にします");

            startvideo.style.display = "none"; // ← ここが超重要
            icon.style.display = "block";
        }
    });

})
