document.addEventListener("DOMContentLoaded", () => {
  // -------------------------
  // DOM取得
  // -------------------------
  const LeftawakeBar     = document.getElementById("LeftawakeBar");
  const RightawakeBar     = document.getElementById("RightawakeBar");
  const LeftpleasureBar  = document.getElementById("LeftpleasureBar");
  const RightpleasureBar  = document.getElementById("RightpleasureBar");
  const gauge        = document.getElementById("emotionArea");
  // const btn          = document.getElementById("showbtn");
  const faceEl       = document.getElementById("emoji-face");
  const labelEl      = document.getElementById("emoji-label");

  const AWAKE_LEFT_COLOR   = "#254FC8"; // 覚醒度マイナス
  const AWAKE_RIGHT_COLOR  = "#E53935"; // 覚醒度プラス

  const PLEASURE_LEFT_COLOR  = "#2FB8C6"; // 快楽度マイナス
  const PLEASURE_RIGHT_COLOR = "#FFB84D"; // 快楽度プラス

  if (!LeftawakeBar || !RightawakeBar || !LeftpleasureBar || !RightpleasureBar || !gauge || !faceEl || !labelEl) {
    console.warn("⚠ ゲージ関連DOMが見つかりません", {
      LeftawakeBar, RightawakeBar,LeftpleasureBar,RightpleasureBar, gauge, btn, faceEl, labelEl
    });
    return;
  }

  // -------------------------
  // 値保持（常にここが正）
  // -------------------------
  window.emotion = window.emotion ?? { x: 0, y: 0 };

  // -------------------------
  // util
  // -------------------------
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n));

  // -1..1 でも 0..100 でも来てもOKにする
  // -2..2 くらいなら「-1..1系」とみなして変換
  const toPercent = (v) => {
    const n = Number(v);
    if (!Number.isFinite(n)) return 0;

    // -1..1 系っぽい
    if (n >= -2 && n <= 2) {
      return clamp((n + 1) * 50, 0, 100);
    }

    // 0..100 系っぽい
    return clamp(n, 0, 100);
  };

  // -------------------------
  // 表情テーブル（emoji + label）
  // -------------------------
  function faceFromArousalValence(awakePct, pleasurePct) {
    const a = clamp(Math.floor(Number(awakePct) / 20), 0, 4);
    const p = clamp(Math.floor(Number(pleasurePct) / 20), 0, 4);

    // 縦=覚醒度, 横=快楽度
    const table = [
      [ {e:"😭", t:"絶望"}, {e:"🫩", t:"しょんぼり"}, {e:"😔", t:"落ち込む"}, {e:"🙂", t:"満足"}, {e:"😀", t:"安心"} ],
      [ {e:"🥲", t:"つらいけど平気"}, {e:"🥺", t:"うるうる"}, {e:"😑", t:"無"}, {e:"😉", t:"余裕"}, {e:"😄", t:"うれしい"} ],
      [ {e:"🙁", t:"不安"}, {e:"😕", t:"困惑"}, {e:"😐", t:"ふつう"}, {e:"😊", t:"にこ"}, {e:"😆", t:"楽しい"} ],
      [ {e:"😠", t:"イラッ"}, {e:"😬", t:"焦り"}, {e:"😋", t:"ノリノリ"}, {e:"😚", t:"上機嫌"}, {e:"🥰", t:"ハッピー"} ],
      [ {e:"🤬", t:"ブチギレ"}, {e:"😡", t:"怒り"}, {e:"😁", t:"ハイテンション"}, {e:"🤩", t:"興奮"}, {e:"🥳", t:"最高潮"} ],
    ];

    return table[a][p]; // {e, t}
  }

  function updateFace(awakePct, pleasurePct) {
    const next = faceFromArousalValence(awakePct, pleasurePct);

    // 絵文字更新（変わった時だけポン）
    if (faceEl.textContent !== next.e) {
      faceEl.textContent = next.e;
      faceEl.classList.remove("pop");
      void faceEl.offsetWidth;
      faceEl.classList.add("pop");
    }

    // ラベル更新
    labelEl.textContent = next.t;
  }

  // -------------------------
  // 描画
  // -------------------------
  window.updateGauge = function () {
    const awakePct = toPercent(window.emotion.x);     // 0..100
    const pleasurePct = toPercent(window.emotion.y); // 0..100
  
    // 初期化
    LeftawakeBar.style.transform  = "scaleX(0)";
    RightawakeBar.style.transform = "scaleX(0)";
    LeftpleasureBar.style.transform  = "scaleX(0)";
    RightpleasureBar.style.transform = "scaleX(0)";
  
    // ===== 覚醒度 =====
    if (awakePct < 50) {
      const scale = (50 - awakePct) / 50; // 0..1
      LeftawakeBar.style.background = AWAKE_LEFT_COLOR;
      LeftawakeBar.style.transform = `scaleX(${scale})`;
    }
  
    if (awakePct > 50) {
      const scale = (awakePct - 50) / 50; // 0..1
      RightawakeBar.style.background = AWAKE_RIGHT_COLOR;
      RightawakeBar.style.transform = `scaleX(${scale})`;
    }
  
    // ===== 快楽度 =====
    if (pleasurePct < 50) {
      const scale = (50 - pleasurePct) / 50;
      LeftpleasureBar.style.background = PLEASURE_LEFT_COLOR;
      LeftpleasureBar.style.transform = `scaleX(${scale})`;
    }
  
    if (pleasurePct > 50) {
      const scale = (pleasurePct - 50) / 50;
      RightpleasureBar.style.background = PLEASURE_RIGHT_COLOR;
      RightpleasureBar.style.transform = `scaleX(${scale})`;
    }
  
    // 表情はそのまま使える
    updateFace(awakePct, pleasurePct);
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
  // gauge.classList.add("hide");

  // if (btn) {
  //   btn.textContent = "ゲージ表示";
  //   btn.addEventListener("click", () => {
  //     gauge.classList.toggle("hide");
  //     btn.textContent = gauge.classList.contains("hide") ? "ゲージ表示" : "ゲージ非表示";
  //   });
  // }
});
