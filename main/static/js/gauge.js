document.addEventListener("DOMContentLoaded", () => {
  // -------------------------
  // DOM取得
  // -------------------------
  const awakeBar     = document.getElementById("awakeBar");
  const pleasureBar  = document.getElementById("pleasureBar");
  const gauge        = document.getElementById("emotionArea");
  const btn          = document.getElementById("showbtn");
  const faceEl       = document.getElementById("emoji-face");
  const labelEl      = document.getElementById("emoji-label");

  if (!awakeBar || !pleasureBar || !gauge || !faceEl || !labelEl) {
    console.warn("⚠ ゲージ関連DOMが見つかりません", {
      awakeBar, pleasureBar, gauge, btn, faceEl, labelEl
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
      [ {e:"😭", t:"絶望"}, {e:"🫩", t:"しょんぼり"}, {e:"😔", t:"落ち込み"}, {e:"🙂", t:"静かに満足"}, {e:"😀", t:"安心"} ],
      [ {e:"🥲", t:"つらいけど平気"}, {e:"🥺", t:"うるうる"}, {e:"😑", t:"無"}, {e:"😉", t:"余裕"}, {e:"😄", t:"うれしい"} ],
      [ {e:"🙁", t:"不安"}, {e:"😕", t:"困惑"}, {e:"😐", t:"ふつう"}, {e:"😊", t:"にこ"}, {e:"😆", t:"楽しい"} ],
      [ {e:"😠", t:"イラッ"}, {e:"😬", t:"焦り"}, {e:"😋", t:"ノリノリ"}, {e:"😚", t:"上機嫌"}, {e:"🥰", t:"ハッピー"} ],
      [ {e:"🤬", t:"ブチギレ"}, {e:"😡", t:"怒り"}, {e:"😁", t:"テンション高"}, {e:"🤩", t:"興奮"}, {e:"🥳", t:"最高潮"} ],
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
    const awakePct    = toPercent(window.emotion.x);
    const pleasurePct = toPercent(window.emotion.y);

    // デバッグ見たい時だけON
    // console.log("RAW:", window.emotion.x, window.emotion.y, "PCT:", awakePct, pleasurePct);

    awakeBar.style.width = awakePct + "%";
    pleasureBar.style.width = pleasurePct + "%";

    // 色（好みで調整してOK）
    awakeBar.style.background = awakePct < 50
      ? "linear-gradient(to right, green)"
      : "linear-gradient(to right, red)";

    pleasureBar.style.background = pleasurePct < 50
      ? "linear-gradient(to right, lightblue)"
      : "linear-gradient(to right, pink)";

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
  gauge.classList.add("hide");

  if (btn) {
    btn.textContent = "ゲージ表示";
    btn.addEventListener("click", () => {
      gauge.classList.toggle("hide");
      btn.textContent = gauge.classList.contains("hide") ? "ゲージ表示" : "ゲージ非表示";
    });
  }
});
