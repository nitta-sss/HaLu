// register_tone.js（新規登録：名前 + トーン取得）
// micStop 後にだけ tone_newuser を呼ぶ決定版

document.addEventListener("DOMContentLoaded", () => {
  const nameEl   = document.getElementById("newUserName");
  const toneBtn  = document.getElementById("tonevoiceBtn");
  const overlayEl = document.getElementById("processingOverlay");

  /* ======================
     UI helpers
  ====================== */
  function showProcessing() {
    if (overlayEl) overlayEl.style.display = "flex";
  }

  function hideProcessing() {
    if (overlayEl) overlayEl.style.display = "none";
  }

  function getNewUserName() {
    return (nameEl?.value || "").trim();
  }

  function refreshButtons() {
    if (!toneBtn) return;

    const hasName = !!getNewUserName();

    if (!state.isRecording) {
      toneBtn.disabled = !hasName;
      toneBtn.textContent = "トーン録音開始";
    } else {
      toneBtn.disabled = false;
      toneBtn.textContent = "トーン録音停止";
    }
  }

  /* ======================
     state（重要）
  ====================== */
  const state = {
    isRecording: false,
    micStopCalled: false,
    gotHz: null
  };

  /* ======================
     mic 制御
  ====================== */
  async function micStart() {
    console.log("🎙️ micStart");
    await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });
    console.log("tonevoiceBtn listener from user_registration.js");

    state.isRecording = true;
    refreshButtons();
  }

  async function micStop() {
    if (state.micStopCalled) {
      console.warn("⚠ micStop 二重防止");
      return;
    }
    state.micStopCalled = true;

    console.log("🛑 micStop");
    await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });

    await onMicStopped();
  }

  /* ======================
     micStop 後にだけ走る処理
  ====================== */
  async function onMicStopped() {
    const user = getNewUserName();
    if (!user) {
      alert("ユーザー名がありません");
      resetState();
      return;
    }

    console.log("🚀 新規トーン登録開始:", user);
    showProcessing();

    try {
      await fetch("http://127.0.0.1:5000/ai/tone_newuser", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user:user })
      });

      console.log("✅ トーン登録完了");

    } catch (err) {
      console.error("❌ tone_newuser error", err);

    } finally {
      hideProcessing();
      resetState();
    }
  }

  /* ======================
     初期化
  ====================== */
  function resetState() {
    state.isRecording = false;
    state.micStopCalled = false;
    state.gotHz = null;
    refreshButtons();
  }

  /* ======================
     イベント
  ====================== */
  nameEl?.addEventListener("input", () => {
    state.gotHz = null;
    refreshButtons();
  });

  toneBtn?.addEventListener("click", async () => {
    const user = getNewUserName();
    if (!user) {
      alert("ユーザー名を入れてね");
      return;
    }

    if (!state.isRecording) {
      await micStart();
    } else {
      await micStop();
    }
  });

  /* ======================
     初期表示
  ====================== */
  resetState();
});
