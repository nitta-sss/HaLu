console.log("emotionPaimon.js loaded");

(() => {
  const video = document.getElementById("sceneVideo");
  if (!video) {
    console.warn("⚠ 画像変更関連DOMが見つかりません", { video });
    return;
  }

  // キャラごとの感情動画
  const sceneMap = {
    forest: {
      normal: "/static/video/Forestpaimon.mp4",
      happy:  "/static/video/a.webm",
      angry:  "/static/video/b.webm",
      sad:    "/static/video/c.webm",
      fun:    "/static/video/d.webm",
    },
  
    ice: {
      normal: "/static/video/IceNormal.webm",
      happy:  "/static/video/b.webm",
      angry:  "/static/video/c.webm",
      sad:    "/static/video/d.webm",
      fun:    "/static/video/a.webm",
    },
  
    flame: {
      normal: "/static/video/FlameNormal.webm",
      happy:  "/static/video/c.webm",
      angry:  "/static/video/d.webm",
      sad:    "/static/video/a.webm",
      fun:    "/static/video/b.webm",
    }
  };

  //中心判定
  const CENTER_THRESHOLD = 0.2;

  // -1..1 に正規化（入力が 0..100 とかでも対応）
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

    //中心ならnormalを返す
    const distance = Math.sqrt(cx * cx + cy * cy);
    if (distance < CENTER_THRESHOLD) {
      return "normal";
    }

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
      console.warn("⚠ emotion値がありません", data);
      return;
    }

    const emotionType = judgeEmotion(x, y);

    // 現在のテーマ（なければ forest）
    const theme = window.currentThemeId || "forest";

    const src = sceneMap[theme]?.[emotionType];

    if (!src) {
      console.warn("⚠ 対応動画なし:", theme, emotionType);
      return;
    }

    changeVideo(src);
  };

  // キャラ変更時にノーマル表情を表示
  window.showNormalFace = function () {

    const theme = window.currentThemeId || "forest";
    const src = sceneMap[theme]?.normal;

    if (!src) {
      console.warn("normal動画がありません:", theme);
      return;
    }

    changeVideo(src);
  };
})();
