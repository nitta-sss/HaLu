console.log("emotionPaimon.js loaded");

(() => {
  const video = document.getElementById("iconVideo");
  if (!video) {
    console.warn("⚠ 画像変更関連DOMが見つかりません", { video });
    return;
  }

  // 感情ごとの動画
  const faceMap = {
    happy: "/static/video/b.webm",   // 喜び
    angry: "/static/video/c.webm", // 怒り
    sad:   "/static/video/d.webm",   // 悲しみ
    fun:   "/static/video/e.webm",   // 楽しみ
  };

  // -1..1 に寄せる（入力が 0..100 とかでも対応）
  function toSigned(v) {
    const n = Number(v);
    if (!Number.isFinite(n)) return 0;

    // -1〜+1 っぽい
    if (n >= -1 && n <= 1) return n;

    // 0〜100 っぽい
    return (n - 50) / 50;
  }

  // dataから x,y を抜く（キー揺れ対応）
  function extractXY(data) {
    // main.js から data を丸ごと渡す前提
    const x = data?.AI_arousal ?? data?.arousal ?? data?.awakening ?? data?.x;
    const y = data?.AI_valence ?? data?.valence ?? data?.pleasure  ?? data?.y;
    return { x, y };
  }

  // 座標で喜怒哀楽を判定
  function judgeEmotion(x, y) {
    const cx = toSigned(x);
    const cy = toSigned(y);

    console.log("覚醒：", x, "快楽：", y, "=> 正規化:", cx, cy);

    if (cx >= 0 && cy >= 0) return "happy"; // 喜
    if (cx >= 0 && cy <= 0) return "angry"; // 怒
    if (cx <  0 && cy <  0) return "sad";   // 哀
    return "fun";                           // 楽
  }

//   動画を安全に切り替える関数
  function changeVideo(src) {
    // すでにこの動画なら何もしない
    if (video.dataset.current === src) return;

    video.dataset.current = src;
  
    video.pause();
    video.src = src;
    video.load();
    video.play().catch(() => {});
  }
  

  // 外部から呼べる関数（dataを受け取る版）
  window.updateFaceByEmotion = function (data) {
    const { x, y } = extractXY(data);

    if (x == null || y == null) {
      console.warn("⚠ 感情値が見つからない", data);
      return;
    }

    const type = judgeEmotion(x, y);
    const src = faceMap[type];

    // // 既に同じ画像なら変更しない
    // if (icon.src.includes(newSrc)) return;

    changeVideo(src);
  };
})();
