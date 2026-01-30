// register_tone.js（新規登録：名前 + トーン取得）
// 取り直しのやり方に合わせた版

document.addEventListener("DOMContentLoaded", () => {
  const nameEl = document.getElementById("newUserName");
  const startBtn = document.getElementById("newUserStart");
  const doneBtn  = document.getElementById("newUserRecDone"); // ★追加ボタン
  const regBtn   = document.getElementById("newUserStop");    // 「登録」
  const statusEl = document.getElementById("userStatus2");

  let isRecording = false;
  let gotHz = null;

  function getNewUserName() {
    if (!nameEl) return "";
    return (nameEl.value || "").trim();
  }

  function setStatus(msg) {
    if (statusEl) statusEl.textContent = msg;
  }

  function refreshButtons() {
    const name = getNewUserName();
    const hasName = !!name;
    const hasHz = (gotHz !== null);

    // 録音してない時：開始だけON（名前あれば）
    if (!isRecording) {
      startBtn.disabled = !hasName;
      if (doneBtn) doneBtn.disabled = true;

      // Hz取れてなければ登録不可
      regBtn.disabled = !hasHz;
      return;
    }

    // 録音中：完了だけON
    startBtn.disabled = true;
    if (doneBtn) doneBtn.disabled = false;

    // 録音中は登録できない
    regBtn.disabled = true;
  }

  // 入力に追従してボタン切り替え
  if (nameEl) {
    nameEl.addEventListener("input", () => {
      // 名前が変わったら、取得済みHzは無効にする（別人のHzになるの防止）
      gotHz = null;
      refreshButtons();
    });
  }

  // status変更に追従（あなたのパターンに合わせて一応付ける）
  if (statusEl) {
    new MutationObserver(refreshButtons)
      .observe(statusEl, { childList: true, characterData: true, subtree: true });
  }

  // 初期状態
  gotHz = null;
  isRecording = false;
  refreshButtons();
  setStatus("ユーザー名を入れて、トーン録音してね");

  // ---- 録音開始 ----
  startBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const name = getNewUserName();
    if (!name) return alert("ユーザー名を入れてね");

    console.log("新規登録 録音開始:", name);

    // 録音開始
    await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });

    isRecording = true;
    setStatus("🎤 トーン録音中…終わったら『トーン録音完了』");
    refreshButtons();
  });

  // ---- 録音完了（停止→Hz取得）----
  if (doneBtn) {
    doneBtn.addEventListener("click", async (e) => {
      e.preventDefault();

      const name = getNewUserName();
      if (!name) return alert("ユーザー名を入れてね");

      console.log("新規登録 録音完了:", name);

      // 録音停止
      await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });

      // ここで「録音結果からHzを算出して返す」APIを叩く
      // 取り直しに合わせた書き方
      await fetch("http://127.0.0.1:5000/ai/tone_newuser", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user: name })
      });

      isRecording = false;
      refreshButtons();
    });
  }

    // 次の登録に備えて初期化
    gotHz = null;
    isRecording = false;
    refreshButtons();

});
