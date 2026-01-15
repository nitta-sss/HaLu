console.log("✅ main.js 読み込まれたよ");

document.addEventListener("DOMContentLoaded", () => {
  let voiceBtn  = document.getElementById("voiceBtn");
  let textInput = document.getElementById("textInput");
  let sendBtn   = document.getElementById("sendBtn");

  if (!voiceBtn) return;

  let isRecording = false;
  let isBusy = false; // AI処理中の連打防止

  // =========================
  // 感情更新（ゲージ.js に丸投げする唯一の入口）
  // =========================
  function applyEmotionFromAI(data) {
    // data から取り出し（候補を広めに対応）
    const arousal  = (data?.arousal  ?? data?.awakening ?? data?.x);
    const valence  = (data?.valence  ?? data?.pleasure  ?? data?.y);

    // どっちもある時だけ反映
    if (arousal == null || valence == null) {
      console.warn("⚠ emotionがレスポンスに無い", data);
      return;
    }

    const x = parseFloat(arousal);
    const y = parseFloat(valence);

    console.log("🎚 emotion update request:", { x, y });

    // ✅ gauge.js の入口を優先
    if (typeof window.updateEmotion === "function") {
      window.updateEmotion(x, y);
      return;
    }

    // フォールバック（古い実装用）
    window.emotion = window.emotion ?? { x: 0, y: 0 };
    window.emotion.x = x;
    window.emotion.y = y;

    if (typeof window.updateGauge === "function") {
      window.updateGauge();
    } else {
      console.warn("⚠ updateGauge が存在しない（gauge.js 読み込み順を確認）");
    }
  }

  // =========================
  // 共通：メッセージ表示 + AI呼び出し + 表示 + 読み上げ
  // =========================
  async function runAIFlow(userText, { speak = true, typeSpeed = 25 } = {}) {
    console.log("runai入った", userText);
    if (!userText) return;

    if (isBusy) return;
    isBusy = true;

    try {
      console.time("AI_FLOW");

      // 1) /ai/run に text を渡す
      const res = await fetch("http://127.0.0.1:5000/ai/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: userText }),
      });

      if (!res.ok) {
        const t = await res.text();
        throw new Error(`/ai/run failed: ${res.status} ${t}`);
      }

      const data = await res.json();
      console.log("AI結果:", data);

      // 2) エラー返ってきた場合
      if (data?.error) {
        addMessage("bot", `⚠ ${data.error}`);
        return;
      }

      // 3) ✅ 感情ゲージ更新（ここが確定）
      applyEmotionFromAI(data);

      // 4) BOT吹き出し（空で作る）
      const botDiv = addMessageElement("bot");

      // 5) 読み上げを先に開始
      let speakPromise = Promise.resolve();
      if (speak) {
        speakPromise = fetch("http://127.0.0.1:5000/ai/speak", { method: "POST" });
      }

      // speak が返るまで待つ（失敗しても継続）
      await speakPromise.catch(() => {});

      // 6) タイプ開始
      const START_DELAY = 1500;
      const TYPE_SPEED = 120;
      await typeWriter(botDiv, String(data.reply ?? ""), TYPE_SPEED, START_DELAY);

      console.timeLog("AI_FLOW", "typing end");
      console.timeEnd("AI_FLOW");
    } catch (err) {
      console.error(err);
      addMessage("bot", "⚠ エラーが発生しました（コンソール確認して）");
    } finally {
      isBusy = false;
    }
  }

  // =========================
  // マイクエラーメッセージ
  // =========================
  function getMicErrorMessage(err) {
    if (!err) return "マイクが使用できません";
    switch (err.name) {
      case "NotFoundError":   return "マイクが接続されていません";
      case "NotAllowedError": return "マイクの使用が許可されていません";
      case "NotReadableError":return "マイクが他のアプリで使用中です";
    }
    if (err.message?.includes("Failed to fetch")) {
      return "音声サーバーに接続できません（サーバーが起動していない可能性があります）";
    }
    switch (err.message) {
      case "MIC_START_FAILED": return "マイクを開始できませんでした";
      case "MIC_STOP_FAILED":  return "マイクを停止できませんでした";
    }
    return "マイクが使用できません";
  }

  // 音声入力ボタン

  let micStream = null;
  let uiStarted = false;

  // マイク存在チェック
  async function checkMicrophone() {
    if (!navigator.mediaDevices?.getUserMedia) {
      throw new Error("BROWSER_NOT_SUPPORTED");
    }
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(t => t.stop());
  }


  function watchMicDisconnect(stream) {
    const track = stream.getAudioTracks()[0];
    if (!track) return;
  
    track.onended = async () => {
      console.warn("🎤 マイクが抜かれました");
  
      if (!isRecording) return;
  
      isRecording = false;
  
      if (uiStarted) {
        window.voiceUI.stop();
        uiStarted = false;
      }
  
      micStream?.getTracks().forEach(t => t.stop());
      micStream = null;

      try {
        await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
      } catch (e) {
        console.error("mic/stop failed after disconnect", e);
      }
  
      showToast("マイクが取り外されました");
    };
  }


  // 音声ボタン
  voiceBtn.addEventListener("click", async () => {
    if (isBusy) return;
    isBusy = true;

    try {
      // START
      if (!isRecording) {
        //開始前チェック
        await checkMicrophone();

        micStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        watchMicDisconnect(micStream);

        const res = await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });
        if (!res.ok) throw new Error("MIC_START_FAILED");

        window.voiceUI.start();
        uiStarted = true;
        isRecording = true;
        return;
      }

      // STOP
      isRecording = false;

      if (uiStarted) {
        window.voiceUI.stop();
        uiStarted = false;
      }

      micStream?.getTracks().forEach(t => t.stop());
      micStream = null;

      const stopRes = await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
      if (!stopRes.ok) throw new Error("MIC_STOP_FAILED");

      const data = await stopRes.json();
      const text = (data.text || "").trim();

      if (!text) {
        addMessage("bot", "⚠ 音声テキストが取得できませんでした");
        return;
      }

      addMessage("user", text);

      // ✅ ここで忙しさ解除してAIへ
      isBusy = false;
      await runAIFlow(text, { speak: true, typeSpeed: 25 });

    } catch (err) {
      console.error(err);

      isRecording = false;
      uiStarted = false;

      micStream?.getTracks().forEach(t => t.stop());
      micStream = null;

      const jp = getMicErrorMessage(err);
      showErrorModal(jp);

    } finally {
      isBusy = false;
    }
  });

  // =========================
  // テキスト送信
  // =========================
  async function sendText() {
    if (isBusy) return;
    isBusy = true;

    const text = (textInput?.value || "").trim();
    if (!text) {
      isBusy = false;
      return;
    }

    textInput.value = "";
    addMessage("user", text);

    isBusy = false;
    await runAIFlow(text, { speak: true, typeSpeed: 30 });
  }

  sendBtn?.addEventListener("click", sendText);
  textInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendText();
  });

});


// =========================
// 表示系ユーティリティ
// =========================
function addMessage(sender, text) {
  console.log("addMessage 呼ばれた:", sender, text);

  const chatBox = document.querySelector(".chat-box");
  if (!chatBox) return;

  const div = document.createElement("div");
  div.className = `balloon ${sender}`;
  div.textContent = text;

  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function addMessageElement(sender) {
  const chatBox = document.querySelector(".chat-box");
  if (!chatBox) return null;

  const div = document.createElement("div");
  div.className = `balloon ${sender}`;
  div.textContent = "";
  chatBox.appendChild(div);

  chatBox.scrollTop = chatBox.scrollHeight;
  return div;
}

function typeWriter(div, fullText, msPerChar, startDelay) {
  return new Promise(resolve => {
    const text = String(fullText ?? "");
    let i = 0;
    const chatBox = document.querySelector(".chat-box");

    setTimeout(function tick() {
      div.textContent += text[i++] ?? "";
      if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;

      if (i >= text.length) return resolve();
      setTimeout(tick, msPerChar);
    }, startDelay);
  });
}
