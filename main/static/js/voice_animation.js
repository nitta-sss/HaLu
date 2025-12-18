window.voiceUI = {
    start() {
        const btn = document.getElementById("voiceBtn");
        if (!btn) return;
        btn.classList.remove("recording-end");
        btn.classList.add("recording");
    },
    stop() {
        const btn = document.getElementById("voiceBtn");
        if (!btn) return;
        btn.classList.remove("recording");
        btn.classList.add("recording-end");
        setTimeout(() => {
            btn.classList.remove("recording-end");
        }, 1750);
    }
};
