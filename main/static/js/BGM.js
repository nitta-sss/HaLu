document.addEventListener("DOMContentLoaded", () => {

    const bgm = document.getElementById("BGMsound");
    const soundBtn = document.getElementById("soundbtn");

    if (!bgm || !soundBtn) return;

    let bgmEnabled = false;

    soundBtn.addEventListener("click", () => {
        if (!bgmEnabled) {
            bgm.volume = 0.5;
            bgm.play().catch(()=>{});
            soundBtn.textContent = "BGMを無効化";
        } else {
            bgm.pause();
            bgm.currentTime = 0;
            soundBtn.textContent = "BGMを有効化";
        }
        bgmEnabled = !bgmEnabled;
    });
});
