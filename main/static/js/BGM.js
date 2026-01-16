document.addEventListener("DOMContentLoaded", () => {
    const bgm = document.getElementById("BGMsound");
    const soundBtn = document.getElementById("soundbtn");
  
    console.log("BGM.js loaded", bgm, soundBtn);
  
    if (!bgm || !soundBtn) {
      console.error("BGM elements not found");
      return;
    }
  
    let bgmEnabled = false;
  
    soundBtn.addEventListener("click", () => {
      if (!bgmEnabled) {
        // alert("BGMを有効化しました");
        bgm.volume = 0.5;
        bgm.play().catch(()=>{});
        soundBtn.textContent = "BGMを無効化";
      } else {
        // alert("BGMを無効化しました");
        bgm.pause();
        bgm.currentTime = 0;
        soundBtn.textContent = "BGMを有効化";
      } 
      bgmEnabled = !bgmEnabled;
    });
  });
  