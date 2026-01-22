// static/js/tone_register.js
document.addEventListener("DOMContentLoaded", () => {
  const toneBtn    = document.getElementById("toneBtn");
  const toneModal  = document.getElementById("toneModal");
  const toneClose  = document.getElementById("toneClose");

  const toneName   = document.getElementById("toneName");
  const toneStatus = document.getElementById("toneStatus");

  const toneStart  = document.getElementById("toneStart");
  const toneStop   = document.getElementById("toneStop");
  const toneRetry  = document.getElementById("toneRetry");

  if (!toneBtn || !toneModal) return;

  // Django(8000)からFlask(5000)を叩く想定。必要ならここを合わせてね。
  const API_BASE = "http://127.0.0.1:5000";

  let isRecording = false;

  function openModal() {
    toneModal.classList.remove("hidden");
    toneStatus.textContent = "ユーザー名を入力して「登録開始」を押してね";
    setButtonsIdle();
  }

  function closeModal() {
    toneModal.classList.add("hidden");
  }

  function setButtonsIdle() {
    isRecording = false;
    toneStart.disabled = false;
    toneStop.disabled  = true;
    toneRetry.disabled = false; // 取り直しは録音してなくても押せるようにしてOK
    toneRetry.textContent = "取り直す";
  }

  function setButtonsRecording() {
    isRecording = true;
    toneStart.disabled = true;
    toneStop.disabled  = false;
    toneRetry.disabled = true;
  }

  function mustName() {
    const name = (toneName.value || "").trim();
    if (!name) {
      toneStatus.textContent = "ユーザー名を入れてね";
      return null;
    }
    return name;
  }

  async function postJson(url, data) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data || {}),
    });
    const json = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = json?.error || `HTTP ${res.status}`;
      throw new Error(msg);
    }
    return json;
  }

  toneBtn.addEventListener("click", openModal);
  toneClose.addEventListener("click", closeModal);

  // 1) 登録開始（録音開始）
  toneStart.addEventListener("click", async () => {
    const name = mustName();
    if (!name) return;

    try {
      toneStatus.textContent = "録音中… 普段の声で2〜3秒しゃべってね";
      setButtonsRecording();

      await postJson(`${API_BASE}/tone/start`, { name });
    } catch (e) {
      toneStatus.textContent = `開始失敗: ${e.message}`;
      setButtonsIdle();
    }
  });

  // 2) 登録完了（録音停止→登録）
  toneStop.addEventListener("click", async () => {
    const name = mustName();
    if (!name) return;

    try {
      toneStatus.textContent = "登録中…";
      const result = await postJson(`${API_BASE}/tone/stop`, { name });

      // result例: { status:"ok", baseline_hz: 142.3 }
      const hz = result?.baseline_hz;
      if (typeof hz === "number") {
        toneStatus.textContent = `登録完了！ ベースライン: ${hz.toFixed(1)}Hz（取り直し可）`;
      } else {
        toneStatus.textContent = "登録完了！（取り直し可）";
      }

      setButtonsIdle();
    } catch (e) {
      toneStatus.textContent = `登録失敗: ${e.message}`;
      setButtonsIdle();
    }
  });

  // 3) 取り直す（= もう一回 start → stop をやる）
  toneRetry.addEventListener("click", () => {
    toneStatus.textContent = "取り直しするなら「登録開始」→「登録完了」をもう一回やってね";
    // 状態はidleのまま
    setButtonsIdle();
  });
});
