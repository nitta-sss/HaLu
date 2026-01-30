console.log("✅ main.js 読み込まれたよ");

document.addEventListener("DOMContentLoaded", () => {

  // delete.js が先に読み込まれててもOK
  window.isResetting = window.isResetting ?? false;

  let voiceBtn  = document.getElementById("voiceBtn");
  let textInput = document.getElementById("textInput");
  let sendBtn   = document.getElementById("sendBtn");

  if (!voiceBtn) return;

  let isRecording = false;
  let isBusy = false;

  // =========================
  // reset中は全部止める（共通ガード）
  // =========================
  function guardReset(label = "") {
    if (window.isResetting) {
      console.log(`🚫 reset中なのでブロック: ${label}`);
      return true;
    }
    return false;
  }

  // =========================
  // 感情更新（gauge.js に丸投げ）
  // =========================
  function applyEmotionFromAI(data) {
    const arousal = (data?.arousal ?? data?.awakening ?? data?.x);
    const valence = (data?.valence ?? data?.pleasure  ?? data?.y);

    if (arousal == null || valence == null) {
      console.warn("⚠ emotionがレスポンスに無い", data);
      return;
    }

    const x = parseFloat(arousal);
    const y = parseFloat(valence);

    console.log("🎚 emotion update request:", { x, y });

    if (typeof window.updateEmotion === "function") {
      window.updateEmotion(x, y);
      return;
    }

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
  // AIフロー
  // =========================
  async function runAIFlow(userText, { speak = true, typeSpeed = 25 } = {}) {
    window.lastUserText = userText;
    if (guardReset("runAIFlow")) return;
  
    console.log("runai入った", userText);
    if (!userText) return;
  
    if (isBusy) return;
    isBusy = true;
  
    const timerLabel = "AI_FLOW";
  
    try {
      console.time(timerLabel);
  
      // 先にユーザー表示（体感も自然）
      addMessage("user", userText);
  
      // ---------- /ai/run ----------
      let runRes;
      try {
        runRes = await fetch("http://127.0.0.1:5000/ai/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: userText }),
        });
      } catch (e) {
        addMessage("bot", "⚠ Flask（Python側）を起動してください");
        console.error("AI server fetch failed:", e);
        return;
      }
  
      if (!runRes.ok) {
        const t = await runRes.text().catch(() => "");
        addMessage("bot", `⚠ AI処理でエラーが発生しました（/ai/run ${runRes.status}）。Flask側のログを確認してください`);
        console.error("/ai/run failed:", runRes.status, t);
        return;
      }
  
      const data = await runRes.json();
  
      // resetが途中で入った場合も止める
      if (guardReset("runAIFlow after /ai/run")) return;
  
      // 感情反映
      applyEmotionFromAI(data);
  
      
      console.log("AI結果:", data);

      // bot吹き出し
      const botDiv = addMessageElement("bot");
      if (!botDiv) return;

      //AI感情動かし
      window.updateFaceByEmotion(data);

      // ←★ここ
      console.log("吹き出し呼ぶ直前");
      window.showCharacterBubble?.(data.reply);
      
      // ---------- /ai/speak ----------
      if (speak) {
        const themeId = window.currentThemeId ?? "forest";
  
        try {
          const speakRes = await fetch("http://127.0.0.1:5000/ai/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ themeId }), // ★Flask側の期待キー
          });
  
          if (!speakRes.ok) {
            addMessage("bot", "⚠ 読み上げに失敗しました。VOICEVOXを起動しているか確認してね");
            console.warn("/ai/speak not ok:", speakRes.status);
          }
        } catch (e) {
          addMessage("bot", "⚠ 読み上げサーバーに接続できません。VOICEVOXを起動してください");
          console.error("speak fetch failed:", e);
        }
      }
  
      // reset中ならタイプも中止
      if (guardReset("typeWriter")) return;
  
      // タイプ演出
      const START_DELAY = 1500;
      const TYPE_SPEED = typeSpeed ?? 120;
      await typeWriter(botDiv, String(data.reply ?? ""), TYPE_SPEED, START_DELAY);
  
    } catch (err) {
      console.error(err);
      addMessage("bot", "⚠ エラーが発生しました（コンソール確認して）");
    } finally {
      // タイマーは必ず閉じる（Timer already exists 防止）
      try { console.timeEnd(timerLabel); } catch (_) {}
      isBusy = false;
    }
  }
  

//マイク入力専用
  async function runAIFlow_voice(userText, { speak = true, typeSpeed = 25 } = {}) {
    window.lastUserText = userText;
    if (guardReset("runAIFlow")) return;
  
    console.log("runai入った", userText);
    if (!userText) return;
  
    if (isBusy) return;
    isBusy = true;
  
    const timerLabel = "AI_FLOW";
  
    try {
      console.time(timerLabel);
  
      // 先にユーザー表示（体感も自然）
      addMessage("user", userText);
  
      // ---------- /ai/run ----------
      let runRes;
      try {
        runRes = await fetch("http://127.0.0.1:5000/ai/run_voice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: userText }),
        });
      } catch (e) {
        addMessage("bot", "⚠ Flask（Python側）を起動してください");
        console.error("AI server fetch failed:", e);
        return;
      }
  
      if (!runRes.ok) {
        const t = await runRes.text().catch(() => "");
        addMessage("bot", `⚠ AI処理でエラーが発生しました（/ai/run ${runRes.status}）。Flask側のログを確認してください`);
        console.error("/ai/run failed:", runRes.status, t);
        return;
      }
  
      const data = await runRes.json();
  
      // resetが途中で入った場合も止める
      if (guardReset("runAIFlow after /ai/run")) return;
  
      // 感情反映
      applyEmotionFromAI(data);
  
      console.log("AI結果:", data);
  
      if (data?.error) {
        addMessage("bot", `⚠ ${data.error}`);
        return;
      }
  
      // bot吹き出し
      const botDiv = addMessageElement("bot");
      if (!botDiv) return;

      //AI感情動かし
      window.updateFaceByEmotion(data);
      
      // ---------- /ai/speak ----------
      if (speak) {
        const themeId = window.currentThemeId ?? "forest";
  
        try {
          const speakRes = await fetch("http://127.0.0.1:5000/ai/speak", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ themeId }), // ★Flask側の期待キー
          });
  
          if (!speakRes.ok) {
            addMessage("bot", "⚠ 読み上げに失敗しました。VOICEVOXを起動しているか確認してね");
            console.warn("/ai/speak not ok:", speakRes.status);
          }
        } catch (e) {
          addMessage("bot", "⚠ 読み上げサーバーに接続できません。VOICEVOXを起動してください");
          console.error("speak fetch failed:", e);
        }
      }
  
      // reset中ならタイプも中止
      if (guardReset("typeWriter")) return;
  
      // タイプ演出
      const START_DELAY = 1500;
      const TYPE_SPEED = typeSpeed ?? 120;
      await typeWriter(botDiv, String(data.reply ?? ""), TYPE_SPEED, START_DELAY);
  
    } catch (err) {
      console.error(err);
      addMessage("bot", "⚠ エラーが発生しました（コンソール確認して）");
    } finally {
      // タイマーは必ず閉じる（Timer already exists 防止）
      try { console.timeEnd(timerLabel); } catch (_) {}
      isBusy = false;
    }
  }

  // =========================
  // マイクエラー文
  // =========================
  function getMicErrorMessage(err) {
    if (!err) return "マイクが使用できません";
    switch (err.name) {
      case "NotFoundError":    return "マイクが接続されていません";
      case "NotAllowedError":  return "マイクの使用が許可されていません";
      case "NotReadableError": return "マイクが他のアプリで使用中です";
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

  // =========================
  // 音声入力
  // =========================
  let micStream = null;
  let uiStarted = false;

  async function checkMicrophone() {
    if (!navigator.mediaDevices?.getUserMedia) throw new Error("BROWSER_NOT_SUPPORTED");
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

  voiceBtn.addEventListener("click", async () => {
    if (guardReset("voiceBtn click")) return;
    if (isBusy) return;
    isBusy = true;

    try {
      // START
      if (!isRecording) {
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

      // reset中なら表示＆AI呼び出しもしない
      if (guardReset("after mic stop")) return;

      //addMessage("user", text);

      // ここで忙しさ解除してAIへ
      isBusy = false;
      await runAIFlow_voice(text, { speak: true, typeSpeed: 25 });

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
      if (guardReset("sendText")) return;
    
      if (window.isBusy) return;
      window.isBusy = true;
      window.updateSendBtnState?.();
    
      const text = textInput.value.trim();
      if (!text) {
        window.isBusy = false;
        window.updateSendBtnState?.();
        return;
      }
    
      textInput.value = "";
      window.updateSendBtnState?.();
    
      await runAIFlow(text, { speak: true, typeSpeed: 30 });
    
      window.isBusy = false;
      window.updateSendBtnState?.();
  }
  

  sendBtn?.addEventListener("click", sendText);
  textInput?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendText();
  });

  document.getElementById("secretLabelBtn")?.addEventListener("click", async () => {
    const text = window.lastUserText || "";
    await fetch("http://127.0.0.1:5000/labeler/open", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ text })
    });
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

// キャラ選択パネル外クリックで閉じる
document.addEventListener("click", (e) => {
  const panel = document.getElementById("bgSelectPanel");
  const icon  = document.querySelector(".icon");
  if (!panel || !icon) return;

  if (panel.classList.contains("hidden")) return;
  if (panel.contains(e.target) || icon.contains(e.target)) return;

  panel.classList.add("hidden");
});

function ensureInitialMessage() {
  const chatBox = document.querySelector(".chat-box");
  if (!chatBox) return false;

  // 既に吹き出しがあるなら何もしない（＝二重防止）
  const hasBalloon = chatBox.querySelector(".balloon");
  if (hasBalloon) return false;

  const first = document.createElement("div");
  first.className = "balloon bot";
  const text = "おいらは森のパイモン。気軽に話しかけてね";

  // チャット欄
  typeWriter(first, text, 60, 300);

  // ⭐ キャラ上の吹き出し
  if (window.showCharacterBubble) {
    window.showCharacterBubble(text, 10000);
  }
  
  chatBox.appendChild(first);
  chatBox.scrollTop = chatBox.scrollHeight;
  return true;
}

// 起動画面、読み込み画面

document.addEventListener("DOMContentLoaded", () => {

  const boot = document.getElementById("bootScreen");
  const bootVideo = document.getElementById("bootVideo");

  const loading = document.getElementById("loadingScreen");
  const loadingVideo = document.getElementById("loadingVideo");

  if (!boot || !loading || !loadingVideo) return;
  
  function enableAllSounds(){
    document.querySelectorAll("audio, video").forEach(media => {
      media.muted = false;
    });
  }

  // 起動画面クリック
  boot.addEventListener("click", () => {
    // 🔊 サイト全体の音を有効化
    enableAllSounds();

    // BGM有効化
    if(window.enableBGM) window.enableBGM();

    // 起動画面停止
    if (bootVideo) bootVideo.pause();
    bootVideo.currentTime = 0;

    // 起動画面を消す
    boot.classList.add("hidden");

    // 読み込み画面表示
    loading.classList.remove("hidden");
    loadingVideo.currentTime = 0;
    loadingVideo.play();

  });

  // 読み込み動画終了 → フェードアウト
  loadingVideo.addEventListener("ended", () => {

    loading.classList.add("fade-out");

    setTimeout(() => {
      loading.remove();   // DOMから完全削除
      ensureInitialMessage(); //最初の文呼び出し(おいらは、、)
    }, 800);

  });

  // 読み込み画面スキップ
  loading.addEventListener("click", ()=>{

    loading.classList.add("fade-out");

    setTimeout(()=>{
      loading.remove();
      ensureInitialMessage(); //最初の文呼び出し(おいらは、、)
    },800);

  });

  const charBubble = document.getElementById("characterBubble");
  const charBubbleText = document.getElementById("characterBubbleText");

  window.showCharacterBubble = function(text, time = 10000){
    if(!charBubble || !charBubbleText){
      console.warn("❌ characterBubble not found");
      return;
    }
  
    // 表示準備
    charBubbleText.textContent = ""; 
    charBubble.classList.remove("hide"); 
    charBubble.classList.add("show");

    clearTimeout(window.charBubbleTimer);

    // タイプ表示（Promiseを使う）
    typeWriter(charBubbleText, String(text ?? ""), 70, 0) .then(() => {
      // ← 全部表示されてから10秒後に消す
      window.charBubbleTimer = setTimeout(() => {
        charBubble.classList.remove("show");
        charBubble.classList.add("hide");
      }, time);
    });
  };
});
