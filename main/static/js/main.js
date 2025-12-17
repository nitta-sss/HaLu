

    

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

    // const startbtn = document.getElementById("startbtn");
    // const startvideo = document.getElementById("startvideo");
    // const icon = document.getElementById("icon");
    // const startArea = document.querySelector(".start-area"); // ← ★先に取る

    // /* 🔄 ページ起動時の初期状態 */
    // startArea.style.display = "none";
    // startvideo.pause();
    // startvideo.currentTime = 0;
    // icon.style.display = "none";

    // startbtn.textContent = "起動";
    // startbtn.disabled = false;

    // /* ▶ 起動ボタン */
    // startbtn.addEventListener("click", () => {
    //     console.log("起動ボタンが押されました");

    //     startbtn.textContent = "起動中";
    //     startbtn.disabled = true;

    //     startvideo.style.display = "block"; // ← 明示的に表示
    //     startvideo.currentTime = 0;
    //     startvideo.play();
    // });

    // /* ▶ 動画の進行監視（これが一番安定） */
    // startvideo.addEventListener("timeupdate", () => {
    //     if (startvideo.currentTime >= startvideo.duration - 0.1) {
    //         console.log("動画を非表示にします");

    //         startvideo.style.display = "none"; // ← ここが超重要
    //         icon.style.display = "block";
    //     }
    // });


