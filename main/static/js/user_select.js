// static/js/user_select.js
// ==============================
// ユーザー選択・保持 完成版
// ==============================

document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://127.0.0.1:5000";

  // localStorage
  const LS_ACTIVE_USER = "halu_active_user";
  const LS_ACTIVE_HZ   = "halu_active_hz";

  // DOM
  const userBtn   = document.getElementById("userBtn");
  const userModal = document.getElementById("userModal");
  const userClose = document.getElementById("userClose");

  const currentUserLabel = document.getElementById("currentUserLabel");
  const currentUserHz    = document.getElementById("currentUserHz");

  const userList   = document.getElementById("userList");
  const userStatus = document.getElementById("userStatus");

  const newUserName  = document.getElementById("newUserName");
  const newUserStart = document.getElementById("newUserStart");
  const newUserStop  = document.getElementById("newUserStop");

  const retryStart = document.getElementById("retryStart");
  const retryStop  = document.getElementById("retryStop");

  if (!userBtn || !userModal) return;

  // グローバル状態
  window.activeUser   = null;
  window.activeUserHz = null;

  let isRecording = false;
  let recordingMode = null;

  // ------------------------------
  // storage
  // ------------------------------
  function loadActiveFromStorage() {
    const u = localStorage.getItem(LS_ACTIVE_USER);
    const hz = Number(localStorage.getItem(LS_ACTIVE_HZ));
    if (u) {
      window.activeUser = u;
      window.activeUserHz = Number.isFinite(hz) ? hz : null;
    }
  }

  function saveActiveToStorage() {
    if (window.activeUser) {
      localStorage.setItem(LS_ACTIVE_USER, window.activeUser);
      if (Number.isFinite(window.activeUserHz)) {
        localStorage.setItem(LS_ACTIVE_HZ, String(window.activeUserHz));
      }
    }
  }

  loadActiveFromStorage();

  // ------------------------------
  // UI
  // ------------------------------
  function setStatus(msg) {
    if (userStatus) userStatus.textContent = msg;
  }

  function setCurrentUserUI() {
    // モーダル内
    if (currentUserLabel) {
      currentUserLabel.textContent = window.activeUser ?? "未選択";
    }
    if (currentUserHz) {
      currentUserHz.textContent =
        Number.isFinite(window.activeUserHz)
          ? `${window.activeUserHz.toFixed(1)} Hz`
          : "-";
    }

    // ヘッダーボタン（★ここが目的）
    userBtn.textContent = window.activeUser
      ? `ユーザー：${window.activeUser}`
      : "ユーザー選択";

    // ボタン制御
    const hasUser = !!window.activeUser;
    if (retryStart) retryStart.disabled = !hasUser || isRecording;
    if (retryStop)  retryStop.disabled  = !hasUser || !isRecording || recordingMode !== "retry";
  }

  function openModal() {
    userModal.classList.remove("hidden");
    setCurrentUserUI();
    refreshUserList();
  }

  function closeModal() {
    userModal.classList.add("hidden");
  }

  // ------------------------------
  // list
  // ------------------------------
  function renderUserList(users) {
    userList.innerHTML = "";

    users.forEach(u => {
      const row = document.createElement("div");
      row.className = "user-item";
      row.textContent = `${u.name}  ${u.baseline_hz.toFixed(1)} Hz`;

      row.addEventListener("click", () => {
        if (isRecording) return;
        window.activeUser = u.name;
        window.activeUserHz = u.baseline_hz;
        saveActiveToStorage();
        setCurrentUserUI();
        setStatus(`選択中：${u.name}`);
      });

      userList.appendChild(row);
    });
  }

  async function refreshUserList() {
    const res = await fetch("/users.txt");
    const text = await res.text();

    const users = text.split(/\r?\n/)
      .filter(Boolean)
      .map(line => {
        const [name, hz] = line.split(/\s+/);
        return { name, baseline_hz: Number(hz) };
      });

    renderUserList(users);
    setStatus("ユーザーを選んでね");
  }

  // ------------------------------
  // events
  // ------------------------------
  userBtn.addEventListener("click", openModal);
  userClose?.addEventListener("click", closeModal);

  setCurrentUserUI(); // ← 初期反映
});
