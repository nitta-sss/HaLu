document.addEventListener("DOMContentLoaded", () => {
    const voiceBtn = document.getElementById("voiceBtn");
    if (!voiceBtn) return;

    let isRecording = false;

    voiceBtn.addEventListener("click", async () => {
        if (!isRecording) {
            isRecording = true;
            window.voiceUI.start();

            await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });

        } else {
            isRecording = false;
            window.voiceUI.stop();

            await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
            await new Promise(r => setTimeout(r, 300));
            await fetch("http://127.0.0.1:5000/ai/run", { method: "POST" });
        }
    });
});
