//エラー対策のテンプレ
document.addEventListener("DOMContentLoaded", () => {

    // HTMLからID取得変数にIN
    const btn = document.getElementById("voiceBtn");

    const seOn = document.getElementById("seOn");
    const seOff = document.getElementById("seOff");

    // 録音ON/OFFの状態を持つ
    let isRecording = false;

    // 録音ONにする
    function startRecording() {
        isRecording = true;     //trueとfalseの反転の代わり

        // SEON
        seOn.currentTime = 0;
        seOn.play();

        console.log("録音ON");

        btn.classList.remove("stop-effect"); // 念のため消す
        btn.classList.add("recording");

        // ここに実際の音声入力開始処理を後で入れる
    }

    // 録音OFFにする
    function stopRecording() {
        isRecording = false;    //trueとfalseの反転の代わり

        //SEOFF
        seOff.currentTime = 0;
        seOff.play();

        console.log("録音OFF");

        btn.classList.remove("recording");

        // OFF時のホワン演出
        btn.classList.add("recording-end");
        setTimeout(() => {
            btn.classList.remove("recording-end");
        }, 500);

        // ここに音声入力停止処理を後で入れる
    }

    // ボタンを押すたびにON/OFF切り替え
    btn.addEventListener("click", () => {
        if (!isRecording) {
            startRecording();
        } else {
            stopRecording();
        }
    });

});
