// エラー対策のテンプレ
document.addEventListener("DOMContentLoaded", () => {

    // HTMLからID取得変数にIN
    const btn = document.getElementById("voiceBtn");
    const face = document.getElementById("faceImg");

    // 初期状態はfalse
        // 録音中かどうか
        let isRecording = false;
        // スペースキー押されているかどうか
        let pressingSpace = false;

    // 音声読み込み
    const startSound = new Audio("/static/sound/start.wav"); 
    const stopSound  = new Audio("/static/sound/stop.wav");

    /* ------------------------
       録音開始
    ------------------------ */
    function startRecording() {

        // isRecordingがtrue（録音中）ならすぐに処理を中止
        // 二重で録音開始されるのを防ぐ
        if (isRecording) return;

        // 録音中というフラグを立て他の処理が「今録音中かどうか」を判定できるようになる
        isRecording = true;

        console.log("録音開始");

        // 音を鳴らす
        startSound.currentTime = 0;
        startSound.play();

        // アニメーション ON
            // ボタン光るアニメーション
            btn.classList.add("recording");
            // 波紋アニメーション
            face.classList.add("face-anim");
    }

    /* ------------------------
       録音停止
    ------------------------ */
    function stopRecording() {
        if (!isRecording) return;
        isRecording = false;

        console.log("録音停止");

        // 音を鳴らす
        stopSound.currentTime = 0;
        stopSound.play();
        
        // アニメーション OFF
        btn.classList.remove("recording");
        face.classList.remove("face-anim");
    }

    /* ------------------------
       ① マウス長押し判定
    ------------------------ */
    // ボタン押したら録音開始
    btn.addEventListener("mousedown", () => {
        startRecording();
    });

    // ボタン話したら録音中止
    btn.addEventListener("mouseup", () => {
        stopRecording();
    });

    /* ------------------------
       ② スペースキー長押し判定
    ------------------------ */

    // 発生イベント→keydown,呼ぶ関数→startRecording()
    document.addEventListener("keydown", (e) => {
        if (e.code === "Space") {
            if (!pressingSpace) {
                pressingSpace = true;
                startRecording();
            }
        }
    });

    // 発生イベント→keyup,呼ぶ関数→stopRecording()
    document.addEventListener("keyup", (e) => {
        if (e.code === "Space") {
            pressingSpace = false;
            stopRecording();
        }
    });

});
