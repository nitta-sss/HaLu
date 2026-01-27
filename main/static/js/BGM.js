document.addEventListener("DOMContentLoaded", () => {
    const bgm = document.getElementById("BGMsound");
    const soundBtn = document.getElementById("soundbtn");
  
    console.log("BGM.js loaded", bgm, soundBtn);
  
    if (!bgm || !soundBtn) {
      console.error("BGM elements not found");
      return;
    }
  
    let bgmEnabled = false;

    window.enableBGM = function(){

      if(bgmEnabled) return;
  
      bgm.volume = 0.5;
      bgm.play().catch(()=>{});
      bgmEnabled = true;
      soundBtn.textContent = "BGMを無効化";
  
    }
  
    window.disableBGM = function(){
  
      if(!bgmEnabled) return;
  
      bgm.pause();
      bgm.currentTime = 0;
      bgmEnabled = false;
      soundBtn.textContent = "BGMを有効化";
  
    }
  
    soundBtn.addEventListener("click", () => {

      if(!bgmEnabled){
        window.enableBGM();
      }else{
        window.disableBGM();
      }
    });
  });
  