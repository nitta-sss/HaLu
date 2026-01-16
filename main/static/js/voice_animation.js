window.voiceUI = {
    start() {
      console.log("voiceUI.start 呼ばれた");

      const btn = document.getElementById("voiceBtn");
      if (!btn) return;
  
      btn.classList.remove("recording-end");
      btn.classList.add("recording");
  
      const se = new Audio("/static/sound/seOnOff.mp3");
      se.currentTime = 0;
      se.play().catch(() => {});
    },
  
    stop() {
      console.log("voiceUI.stop 呼ばれた"); 

      const btn = document.getElementById("voiceBtn");
      if (!btn) return;
  
      btn.classList.remove("recording");
      btn.classList.add("recording-end");
  
      const se = new Audio("/static/sound/seOnOff.mp3");
      se.currentTime = 0;
      se.play().catch(() => {});
  
      setTimeout(() => {
        btn.classList.remove("recording-end");
      }, 1750);
    }
  };
  