document.addEventListener("DOMContentLoaded", () => {
    // -------------------------
    // DOM取得
    // -------------------------
    const awakeBar     = document.getElementById("awakeBar");
    const pleasureBar  = document.getElementById("pleasureBar");
    const gauge        = document.getElementById("emotionArea");
    const btn          = document.getElementById("showbtn");
    const faceEl       = document.getElementById("emoji-face");
  
    if (!awakeBar || !pleasureBar || !gauge || !faceEl) {
      console.warn("⚠ ゲージ関連DOMが見つかりません", { awakeBar, pleasureBar, gauge, btn, faceEl });
      return;
    }
  
    // -------------------------
    // 値保持（常にここが正）
    // -------------------------
    window.emotion = window.emotion ?? { x: 0, y: 0 };
  
    // -------------------------
    // normalize: -1..1 → 0..100
    // -------------------------
    const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
    const normalize = (v) => clamp((Number(v) + 1) * 50, 0, 100);
  
    // -------------------------
    // 顔テーブル
    // -------------------------
    function faceFromArousalValence(awake, pleasure) {
      const a = clamp(Math.floor(Number(awake) / 20), 0, 4);
      const p = clamp(Math.floor(Number(pleasure) / 20), 0, 4);
  
      //縦が覚醒度、横が快楽度（0.4刻みで表情が変わる）
      const table = [
        ["😭","🫩","😔","🙂","😀"],
        ["🥲","🥺","😑","😉","😄"],
        ["🙁","😕","😐","😊","😆"],
        ["😠","😬","😋","😚","🥰"],
        ["🤬","😡","😁","🤩","🥳"],
      ];
      return table[a][p];
    }
  
    function updateFace(awake, pleasure) {
      const next = faceFromArousalValence(awake, pleasure);
      if (faceEl.textContent !== next) {
        faceEl.textContent = next;
        faceEl.classList.remove("pop");
        void faceEl.offsetWidth;
        faceEl.classList.add("pop");
      }
    }
  
    // -------------------------
    // 描画
    // -------------------------
    window.updateGauge = function () {
      const awake    = normalize(window.emotion.x);
      const pleasure = normalize(window.emotion.y);
  
      // デバッグ見たい時だけON
      console.log("RAW:", window.emotion.x, window.emotion.y, "NORM:", awake, pleasure);
  
      awakeBar.style.width = awake + "%";
      pleasureBar.style.width = pleasure + "%";
  
      awakeBar.style.background = awake < 50
        ? "linear-gradient(to right, green)"
        : "linear-gradient(to right, red)";
  
      pleasureBar.style.background = pleasure < 50
        ? "linear-gradient(to right, lightblue)"
        : "linear-gradient(to right, pink)";
  
      updateFace(awake, pleasure);
    };
  
    // -------------------------
    // 外部から更新する唯一の入口
    // -------------------------
    window.updateEmotion = function (x, y) {
      window.emotion.x = x;
      window.emotion.y = y;
      window.updateGauge();
    };
  
    // -------------------------
    // 初期化
    // -------------------------
    window.updateGauge();
    gauge.classList.add("hide");
  
    if (btn) {
      btn.textContent = "ゲージ表示";
      btn.addEventListener("click", () => {
        gauge.classList.toggle("hide");
        btn.textContent = gauge.classList.contains("hide") ? "ゲージ表示" : "ゲージ非表示";
      });
    }
  });
  