// register_tone.js（新規登録：名前 + トーン取得）
// 取り直しのやり方に合わせた版

document.addEventListener("DOMContentLoaded", () => {
  const nameEl = document.getElementById("newUserName");
  const toneBtn   = document.getElementById("tonevoiceBtn");
  // const statusEl = document.getElementById("userStatus2");

  const overlayEl = document.getElementById("processingOverlay");

  function showProcessing() {
    if (overlayEl) overlayEl.style.display = "flex";
  }

  function hideProcessing() {
    if (overlayEl) overlayEl.style.display = "none";
  }

  let isRecording = false;
  let gotHz = null;

  function getNewUserName() {
    if (!nameEl) return "";
    return (nameEl.value || "").trim();
  }

  // function setStatus(msg) {
  //   if (statusEl) statusEl.textContent = msg;
  // }

  function refreshButtons() {
    if (!toneBtn) return;

    const hasName = !!getNewUserName();

    // 録音していない状態
    if (!isRecording) {
      toneBtn.disabled = !hasName;
      toneBtn.textContent = "トーン録音開始";
      return;
    }

    // 録音中
    toneBtn.disabled = false;
    toneBtn.textContent = "トーン録音停止";
  }


  // 入力に追従してボタン切り替え
  if (nameEl) {
    nameEl.addEventListener("input", () => {
      // 名前が変わったら、取得済みHzは無効にする（別人のHzになるの防止）
      gotHz = null;
      refreshButtons();
    });
  }

  // 初期状態
  gotHz = null;
  isRecording = false;
  let uiStarted = false;
  let micStream = null;
  refreshButtons();

  toneBtn.addEventListener("click", async () => {
  const user = getNewUserName();
  if (!user) return alert("ユーザー名を入れてね");

  // START
  if (!isRecording) {
    await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });
    isRecording = true;
    refreshButtons();
    return;
  }

  // STOP
  await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });

  showProcessing();
  await fetch("http://127.0.0.1:5000/ai/tone_newuser", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user })
  });
  hideProcessing();

  isRecording = false;
  refreshButtons();
});

  

  console.log("新規トーンストップ")
  // ★ 処理中ウィンドウ表示
  showProcessing();

  try {
      fetch("http://127.0.0.1:5000/ai/tone_newuser", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user: getNewUserName() })
      });

  } catch (err) {
    console.error(err);
  } finally {
    // ★ 処理終了 → ウィンドウを消す
    hideProcessing();
    isRecording = false;
    refreshButtons();
  }

  

    // 次の登録に備えて初期化
    gotHz = null;
    isRecording = false;
    refreshButtons();

});
