console.log("✅ user_select.js loaded");
// static/js/user_select.js
// ==============================
// ユーザー選択・保持 完成版
// ==============================

document.addEventListener("DOMContentLoaded", () => {
  const API_BASE = "http://127.0.0.1:5000";

  // localStorage
  const LS_ACTIVE_USER = "halu_active_user";
  const LS_ACTIVE_HZ   = "halu_active_hz";

  let tempUser = null;
  let tempUserHz = null;


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

  // if (!userBtn || !userModal) return;

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

    // 今の確定ユーザーを仮選択に入れる
    tempUser = window.activeUser;
    tempUserHz = window.activeUserHz;

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
    console.log("activeUser =", window.activeUser);
    userList.innerHTML = "";

    users.forEach(u => {
      const row = document.createElement("div");
      row.className = "user-item";

      const nameSpan = document.createElement("span");
      nameSpan.textContent = `${u.name} : ${u.baseline_hz.toFixed(1)} Hz`;
      row.appendChild(nameSpan);

      // ===== 使用中ユーザー =====
      if (u.name === window.activeUser) {
        const using = document.createElement("span");
        using.textContent = "使用中";
        using.className = "using-label";
        row.appendChild(using);
      } else {
        // ===== 変更ボタン =====
        const changeBtn = document.createElement("button");
        changeBtn.textContent = "変更";
        changeBtn.className = "button-32"; 
        changeBtn.addEventListener("click", () => {
          // ボタンクリック時に activeUser を変更
          window.activeUser = u.name;
          window.activeUserHz = u.baseline_hz; // Hz も合わせる

          setCurrentUserUI(); // ← これを追加！ヘッダー表示を更新
          renderUserList(users); // 再描画して「使用中」と変更ボタンを更新
        });
        row.appendChild(changeBtn);
      }

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
  userClose?.addEventListener("click", () => {
    if (tempUser) {
      window.activeUser = tempUser;
      window.activeUserHz = tempUserHz;
      saveActiveToStorage();
    }

    setCurrentUserUI();
    refreshUserList(); 
    closeModal();

    console.log("ユーザー選択：",activeUser)
    fetch("http://127.0.0.1:5000/ai/tone", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({activeUser: window.activeUser,
                            activeUserHz:window.activeUserHz 
       }),
    });
    
  });

  
  setCurrentUserUI(); // ← 初期反映
});
