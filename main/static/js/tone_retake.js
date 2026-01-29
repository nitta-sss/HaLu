document.addEventListener("DOMContentLoaded", () => {
  const retakeStartBtn = document.getElementById("retryStart");
  const retakeFinishBtn = document.getElementById("retryStop");


  let selectedUser = "";

  // user_select.js が作った user-row を利用
  document.getElementById("userList").addEventListener("click", (e) => {
    const row = e.target.closest(".user-row");
    if (!row) return;
    selectedUser = row.dataset.user;
  });

  retakeStartBtn.addEventListener("click", () => {
    if (!selectedUser) {
      alert("ユーザーを選んでね");
      return;
    }
    console.log("取り直し開始:", selectedUser);
    fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });
  });

  retakeFinishBtn.addEventListener("click", async () => {
    if (!selectedUser) {
      alert("ユーザーを選んでね");
      return;
    }

    fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });

    const res = await fetch("/ai/tone_retake_finish", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({user: selectedUser})
    });

    const data = await res.json();
    console.log("新Hz:", data.hz);
  });
});
