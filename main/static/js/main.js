console.log("✅ main.js 読み込まれたよ");

document.addEventListener("DOMContentLoaded", () => {
  const voiceBtn  = document.getElementById("voiceBtn");
  const textInput = document.getElementById("textInput");
  const sendBtn   = document.getElementById("sendBtn");

  if (!voiceBtn) return;

  let isRecording = false;
  let isBusy = false; // AI処理中の連打防止

  // =========================
  // 共通：メッセージ表示 + AI呼び出し + 表示 + 読み上げ
  // =========================
  async function runAIFlow(userText, { speak = true, typeSpeed = 25 } = {}) {
    if (!userText) return;

    // すでに処理中なら弾く（任意）
    if (isBusy) return;
    isBusy = true;

    try {
      console.time("AI_FLOW");

      // 1) /ai/run に text を渡す（重要）
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

      // 3) 感情ゲージ更新
      if (data.arousal != null && data.valence != null) {
        window.emotion.x = parseFloat(data.arousal);
        window.emotion.y = parseFloat(data.valence);
        window.updateGauge?.();
      }



      const botDiv = addMessageElement("bot");

      let speakPromise = Promise.resolve();
      if (speak) {
        speakPromise = fetch("http://127.0.0.1:5000/ai/speak", { method: "POST" });
      }

      // speak が返ってくるまで待つ（＝Flask側の処理が返るまで）
      await speakPromise.catch(() => {});

      // その後にタイプ開始
      const START_DELAY = 1500;
      const TYPE_SPEED =120
      await typeWriter(botDiv, String(data.reply ?? ""), TYPE_SPEED,START_DELAY);

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
  // 音声ボタン
  // =========================
  voiceBtn.addEventListener("click", async () => {
    // AI処理中に録音開始させない（任意）
    if (isBusy) return;

    try {
      if (!isRecording) {
        isRecording = true;

        // 見た目：録音中クラス
        voiceBtn.classList.add("recording");

        window.voiceUI?.start();

        const res = await fetch("http://127.0.0.1:5000/mic/start", { method: "POST" });
        if (!res.ok) throw new Error(`/mic/start failed: ${res.status}`);
        return;
      }

      // ---- stop ----
      isRecording = false;

      voiceBtn.classList.remove("recording");
      voiceBtn.classList.add("recording-end");
      setTimeout(() => voiceBtn.classList.remove("recording-end"), 1800);

      window.voiceUI?.stop();

      const stopRes = await fetch("http://127.0.0.1:5000/mic/stop", { method: "POST" });
      if (!stopRes.ok) throw new Error(`/mic/stop failed: ${stopRes.status}`);

      const stopData = await stopRes.json();
      console.log("mic/stop 結果:", stopData);

      // 先にユーザー文を表示
      const userText = (stopData.text || "").trim();
      if (userText) {
        addMessage("user", userText);
      } else {
        addMessage("bot", "⚠ 音声テキストが取得できませんでした");
        return;
      }

      // ちょい待ち（UI安定用）
      await new Promise(r => setTimeout(r, 200));

      // AI処理（textを渡す！）
      await runAIFlow(userText, { speak: true, typeSpeed: 25 });

    } catch (err) {
      console.error(err);
      addMessage("bot", "⚠ マイク処理でエラーが出ました（コンソール確認）");

      // 状態復旧
      isRecording = false;
      voiceBtn.classList.remove("recording");
    }
  });

  // =========================
  // テキスト送信（マイク横）
  // =========================
  async function sendText() {
    const text = (textInput?.value || "").trim();
    if (!text) return;

    // 入力欄クリア + 表示
    textInput.value = "";
    addMessage("user", text);

    // AI処理へ
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
  div.textContent = ""; // 空で作る
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
      div.textContent += text[i++];
      if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;

      if (i >= text.length) return resolve();

      setTimeout(tick, msPerChar);
    }, startDelay);
  });
}


