// static/js/user_select.js
// ==============================
// 「ユーザー選択」ボタン1つで全部：
//  - 一覧表示（名前 + 平均トーン）
//  - ユーザーを押すとそのユーザーが選択され、平均トーンも適用
//  - 新規登録（ユーザー名 + トーン登録）
//  - 既存ユーザーのトーン取り直し（上書き）
//  - 選択状態は localStorage に保存（ページ更新しても復元）
// ==============================

document.addEventListener("DOMContentLoaded", () => {
  // ===== Flask のベースURL（環境に合わせて変更）=====
  const API_BASE = "http://127.0.0.1:5000";

  // ===== localStorage キー =====
  const LS_ACTIVE_USER = "halu_active_user";
  const LS_ACTIVE_HZ = "halu_active_hz";

  // ===== DOM =====
  const userBtn = document.getElementById("userBtn");
  const userModal = document.getElementById("userModal");
  const userClose = document.getElementById("userClose");

  const currentUserLabel = document.getElementById("currentUserLabel");
  const currentUserHz = document.getElementById("currentUserHz");

  const userList = document.getElementById("userList");
  const userStatus = document.getElementById("userStatus");

  const newUserName = document.getElementById("newUserName");
  const newUserStart = document.getElementById("newUserStart");
  const newUserStop = document.getElementById("newUserStop");

  const retryStart = document.getElementById("retryStart");
  const retryStop = document.getElementById("retryStop");

  if (!userBtn || !userModal) return;

  // ===== グローバル（他JSから参照可能）=====
  window.activeUser = window.activeUser ?? null;
  window.activeUserHz = window.activeUserHz ?? null;

  // ===== 状態 =====
  let isRecording = false;
  let recordingTargetName = null; // 録音対象ユーザー
  let recordingMode = null;       // "new" | "retry" | null

  // ------------------------------
  // storage
  // ------------------------------
  function loadActiveFromStorage() {
    const u = localStorage.getItem(LS_ACTIVE_USER);
    const hzRaw = localStorage.getItem(LS_ACTIVE_HZ);

    if (u && u.trim()) {
      window.activeUser = u.trim();
      const hz = Number(hzRaw);
      window.activeUserHz = Number.isFinite(hz) ? hz : null;
    }
  }

  function saveActiveToStorage() {
    if (window.activeUser) {
      localStorage.setItem(LS_ACTIVE_USER, String(window.activeUser));
      if (typeof window.activeUserHz === "number" && Number.isFinite(window.activeUserHz)) {
        localStorage.setItem(LS_ACTIVE_HZ, String(window.activeUserHz));
      } else {
        localStorage.removeItem(LS_ACTIVE_HZ);
      }
    } else {
      localStorage.removeItem(LS_ACTIVE_USER);
      localStorage.removeItem(LS_ACTIVE_HZ);
    }
  }

  // 起動時に復元
  loadActiveFromStorage();

  // ------------------------------
  // fetch helper
  // ------------------------------
  async function getJson(url) {
    const res = await fetch(url, { method: "GET" });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(json?.error || `HTTP ${res.status}`);
    return json;
  }

  async function postJson(url, data) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data || {}),
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(json?.error || `HTTP ${res.status}`);
    return json;
  }

  // ------------------------------
  // UI
  // ------------------------------
  function escapeHtml(s) {
    return String(s ?? "").replace(/[&<>"']/g, (m) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[m]));
  }

  function setStatus(msg) {
    if (userStatus) userStatus.textContent = msg;
  }

  function setCurrentUserUI() {
    if (currentUserLabel) currentUserLabel.textContent = window.activeUser ?? "未選択";
    if (currentUserHz) {
      currentUserHz.textContent =
        typeof window.activeUserHz === "number" && Number.isFinite(window.activeUserHz)
          ? `${window.activeUserHz.toFixed(1)} Hz`
          : "-";
    }

    // 取り直しボタンの有効化
    const hasUser = !!window.activeUser;
    if (retryStart) retryStart.disabled = !hasUser || isRecording;
    if (retryStop) retryStop.disabled = !hasUser || !isRecording || recordingMode !== "retry";
  }

  function setNewButtonsState() {
    if (!newUserStart || !newUserStop) return;

    // 新規登録用
    newUserStart.disabled = isRecording; // 録音中は開始不可
    newUserStop.disabled = !isRecording || recordingMode !== "new";
  }

  function resetRecordingState() {
    isRecording = false;
    recordingTargetName = null;
    recordingMode = null;
    setCurrentUserUI();
    setNewButtonsState();
  }

  function openModal() {
    userModal.classList.remove("hidden");
    setCurrentUserUI();
    setNewButtonsState();
    setStatus("ユーザー一覧を読み込み中…");
    refreshUserList();
  }

  function closeModal() {
    userModal.classList.add("hidden");
  }

  // ------------------------------
  // list / render
  // ------------------------------
  function renderUserList(users) {
    if (!userList) return;
    userList.innerHTML = "";

    if (!users || users.length === 0) {
      userList.innerHTML = `<div style="opacity:.8;">まだユーザーがいません（下で新規登録してね）</div>`;
      return;
    }

    users.forEach((u) => {
      const name = String(u?.name ?? "").trim();
      const hzNum = typeof u?.baseline_hz === "number" ? u.baseline_hz : Number(u?.baseline_hz);
      const hzOk = Number.isFinite(hzNum);

      const row = document.createElement("div");
      row.className = "user-item";

      // ✅ 重要：表示の右側に平均トーンが入っていても確実に取れるように dataset に埋め込む
      row.dataset.name = name;
      row.dataset.hz = hzOk ? String(hzNum) : "";

      row.innerHTML = `
        <div class="name">${escapeHtml(name)}</div>
        <div class="hz">${hzOk ? hzNum.toFixed(1) + " Hz" : "-"}</div>
      `;

      row.addEventListener("click", () => {
        // 録音中は切り替え禁止（事故防止）
        if (isRecording) {
          setStatus("録音中はユーザー切り替えできないよ（いったん登録完了してね）");
          return;
        }

        const selectedName = row.dataset.name || name;
        const hz = Number(row.dataset.hz);

        window.activeUser = selectedName;
        window.activeUserHz = Number.isFinite(hz) ? hz : null;
        saveActiveToStorage();

        setCurrentUserUI();
        setStatus(`選択中：${selectedName}`);
      });

      userList.appendChild(row);
    });
  }

  async function refreshUserList() {
    try {
      // Flask: GET /tone/users -> { users: [{name, baseline_hz}, ...] }
      const data = await getJson(`${API_BASE}/tone/users`);
      renderUserList(data.users);

      // 現在選択中ユーザーが一覧にいない場合はHzだけ不明になることがあるので、
      // 一覧から補完しておく（任意だけど便利）
      if (window.activeUser && (!Number.isFinite(window.activeUserHz))) {
        const hit = (data.users || []).find((u) => String(u?.name ?? "").trim() === window.activeUser);
        if (hit && Number.isFinite(Number(hit.baseline_hz))) {
          window.activeUserHz = Number(hit.baseline_hz);
          saveActiveToStorage();
          setCurrentUserUI();
        }
      }

      setStatus("ユーザーを選ぶか、新規登録してね");
    } catch (e) {
      setStatus(`一覧取得失敗: ${e.message}`);
    }
  }

  // ------------------------------
  // recording flow
  // ------------------------------
  async function startToneRegistration(name, mode /* "new" | "retry" */) {
    const nm = String(name ?? "").trim();
    if (!nm) {
      setStatus("ユーザー名を入れてね");
      return;
    }
    if (isRecording) {
      setStatus("すでに録音中だよ");
      return;
    }

    try {
      isRecording = true;
      recordingTargetName = nm;
      recordingMode = mode;

      setCurrentUserUI();
      setNewButtonsState();

      if (mode === "new") {
        setStatus("🎤 新規登録：録音中… 普段の声で2〜3秒しゃべってね");
      } else {
        setStatus("🎤 取り直し：録音中… 普段の声で2〜3秒しゃべってね");
      }

      // Flask: POST /tone/start {name}
      await postJson(`${API_BASE}/tone/start`, { name: nm });

      // ボタン状態を反映
      setCurrentUserUI();
      setNewButtonsState();
    } catch (e) {
      setStatus(`録音開始失敗: ${e.message}`);
      resetRecordingState();
    }
  }

  async function stopToneRegistration() {
    if (!isRecording || !recordingTargetName) {
      setStatus("録音中じゃないよ");
      return;
    }

    try {
      setStatus("登録中…");

      // Flask: POST /tone/stop {name} -> {name, baseline_hz}
      const data = await postJson(`${API_BASE}/tone/stop`, { name: recordingTargetName });

      const nm = String(data?.name ?? recordingTargetName).trim();
      const hz = Number(data?.baseline_hz);

      // 登録したユーザーを自動で選択中にする（UX良）
      window.activeUser = nm;
      window.activeUserHz = Number.isFinite(hz) ? hz : null;
      saveActiveToStorage();

      setStatus(
        Number.isFinite(window.activeUserHz)
          ? `登録完了：${nm} / ${window.activeUserHz.toFixed(1)} Hz`
          : `登録完了：${nm}`
      );

      resetRecordingState();
      await refreshUserList();
    } catch (e) {
      setStatus(`登録失敗: ${e.message}`);
      resetRecordingState();
    }
  }

  // ------------------------------
  // events
  // ------------------------------
  userBtn.addEventListener("click", openModal);
  if (userClose) userClose.addEventListener("click", closeModal);

  // 新規登録：開始
  if (newUserStart) {
    newUserStart.addEventListener("click", () => {
      const name = String(newUserName?.value ?? "").trim();
      if (!name) return setStatus("新しいユーザー名を入力してね");
      startToneRegistration(name, "new");
    });
  }

  // 新規登録：完了
  if (newUserStop) {
    newUserStop.addEventListener("click", () => {
      stopToneRegistration();
    });
  }

  // 取り直し：開始（選択中ユーザー）
  if (retryStart) {
    retryStart.addEventListener("click", () => {
      if (!window.activeUser) return setStatus("先にユーザーを選んでね");
      startToneRegistration(window.activeUser, "retry");
    });
  }

  // 取り直し：完了
  if (retryStop) {
    retryStop.addEventListener("click", () => {
      stopToneRegistration();
    });
  }

  // 初期UI反映（モーダル外でも currentUserLabel を出してるなら即反映される）
  setCurrentUserUI();
});
