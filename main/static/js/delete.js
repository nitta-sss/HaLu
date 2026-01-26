// delete.js（完全版）
console.log("🔥 delete.js VERSION = 2026-01-16 A");

document.addEventListener("DOMContentLoaded", () => {
  console.log("① delete.js DOMContentLoaded");

  const btn = document.getElementById("deleteHistoryBtn");
  console.log("② deleteHistoryBtn:", btn);

  if (!btn) return;

  btn.addEventListener("click", async () => {
    console.log("③ 削除ボタン クリック");

    const ok = confirm("本当に会話履歴を削除しますか？\nこの操作は元に戻せません。");
    console.log("④ confirm:", ok);
    if (!ok) return;

    // まずUIを消す（ここが一番体感ある）
    const cleared = clearChatUI();
    console.log("⑤ clearChatUI 結果:", cleared);

    // 入力欄も初期化
    const input = document.getElementById("textInput");
    if (input) input.value = "";
    console.log("⑥ input clear");

    // 感情も初期化（任意）
    if (typeof window.updateEmotion === "function") {
      window.updateEmotion(0, 0);
      console.log("⑦ updateEmotion(0,0)");
    } else {
      console.log("⑦ updateEmotion なし");
    }

    // 🔹 履歴削除時に動画を normal に戻す
    if (typeof window.showNormalFace === "function") {
      window.showNormalFace();
      console.log("⑦-2 showNormalFace 呼び出し");
    }

    // 連打防止（任意：main.js側で見てるなら効く）
    window.isResetting = true;
    console.log("⑧ isResetting = true");

    // Flaskの会話履歴を削除
    try {
      console.log("⑨ fetch Flask /ai/reset start");
      const res = await fetch("http://127.0.0.1:5000/ai/reset", { method: "POST" });
      console.log("⑩ fetch res:", res.status);

      if (!res.ok) {
        const t = await res.text();
        console.log("⑪ res text:", t);
        alert("サーバー側の削除に失敗（コンソール見て）");
        return;
      }

      const data = await res.json().catch(() => ({}));
      console.log("⑫ reset json:", data);

    } catch (e) {
      console.error("⑬ fetch error:", e);
      alert("Flaskに繋がらないっぽい（起動してる？）");
    } finally {
      window.isResetting = false;
      console.log("⑭ isResetting = false");
    }
  });
});


// =========================
// 左チャットDOMを強制削除
// =========================
function clearChatUI() {
  const chatBox = document.querySelector(".chat-box");
  console.log("A chatBox:", chatBox);

  if (!chatBox) return { ok: false, reason: "chatBox not found" };

  const before = chatBox.querySelectorAll(".balloon").length;
  console.log("B balloons before:", before);

  // 100%消す（Djangoで描いた分も、JSで足した分も）
  chatBox.querySelectorAll(".balloon").forEach(el => el.remove());

  const after = chatBox.querySelectorAll(".balloon").length;
  console.log("C balloons after:", after);

  ensureInitialMessage();//最初の文呼び出し(おいらは、、)

  return { ok: true, before, after };
}
