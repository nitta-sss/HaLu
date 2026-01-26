document.addEventListener("DOMContentLoaded", () => {

    // 🔹 トリガー：左上アイコン
    const triggerIcon = document.querySelector(".icon");

    // 🔹 変更対象
    const charaName = document.querySelector(".character-name");
    const charaPersonality = document.querySelector(".character-personality");

    // 🔹 選択パネル
    const panel = document.getElementById("bgSelectPanel");

    if (
        !triggerIcon ||
        !charaName ||
        !charaPersonality ||
        !panel
    ) 
        return;

    // 🔹 アイコンクリック → パネル表示切替
    triggerIcon.addEventListener("click", () => {
        panel.classList.toggle("hidden");
    });

    // 🔹 テーマ選択処理
    document.querySelectorAll(".bg-card").forEach(card => {
        card.addEventListener("click", () => {
  
            const name = card.dataset.name;
            const personality = card.dataset.personality;
            const themeId = card.id; // Forest / ice など

            // -----------------
            // 名前・説明変更
            // -----------------
            charaName.textContent = name;
            charaPersonality.textContent = personality;

            // 名前・説明文変更
            charaName.textContent = name;
            charaPersonality.textContent = personality;

            // ★ ここが今回の本題：idをそのままclassにする
            charaName.className = `character-name ${themeId}`;
            charaPersonality.className = `character-personality ${themeId}`;

            // 🌍 グローバルに公開
            window.currentThemeId = themeId;
            window.showNormalFace?.();

            // パネルを閉じる
            panel.classList.add("hidden");
        });
    });
});
