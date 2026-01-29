document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("retryStart");
  const stopBtn  = document.getElementById("retryStop");
  const userStatusEl = document.getElementById("userStatus");

  let isRecording = false;

  function getSelectedUserFromStatus() {
    if (!userStatusEl) return "";
    const text = (userStatusEl.textContent || "").trim();
    const m = text.match(/^選択中（未確定）：\s*(.+)\s*$/);
    if (!m) return "";
    return m[1].trim(); // *付きでも返す
  }

  function refreshButtons() {
    const selectedUser = getSelectedUserFromStatus();
    const hasUser = !!selectedUser;

    // 録音してない時：開始だけON（ユーザー選択できてれば）
    if (!isRecording) {
      startBtn.disabled = !hasUser;
      stopBtn.disabled  = true;
      return;
    }

    // 録音中：完了だけON
    startBtn.disabled = true;
    stopBtn.disabled  = false;
  }

  // user_select.js の表示更新に追従
  if (userStatusEl) {
    new MutationObserver(refreshButtons)
      .observe(userStatusEl, { childList: true, characterData: true, subtree: true });
  }

  refreshButtons();

  startBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const selectedUser = getSelectedUserFromStatus();
    if (!selectedUser) return alert("ユーザーを選んでね");

    console.log("取り直し開始:", selectedUser);

    await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });

    isRecording = true;
    refreshButtons();
  });

  stopBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const selectedUser = getSelectedUserFromStatus();
    if (!selectedUser) return alert("ユーザーを選んでね");

    text = await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
    console.log("tone_retake.js",text)
    const res = await fetch("http://127.0.0.1:5000/ai/tone_retake", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: selectedUser.replace("*", "").trim() })
    });

    const data = await res.json();
    console.log("新Hz:", data.hz);

    isRecording = false;
    refreshButtons();
  });
});
