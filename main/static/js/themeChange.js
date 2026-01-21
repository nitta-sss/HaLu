document.addEventListener("DOMContentLoaded", () => {

    // 🔹 トリガー：左上アイコン
    const triggerIcon = document.querySelector(".icon");

    // 🔹 変更対象
    const bgImg = document.querySelector(".right-back");
    const charaImg = document.getElementById("icon"); // 右側キャラ
    const charaName = document.querySelector(".character-name");
    const charaPersonality = document.querySelector(".character-personality");

    // 🔹 選択パネル
    const panel = document.getElementById("bgSelectPanel");

    if (
        !triggerIcon ||
        !bgImg ||
        !charaImg ||
        !charaName ||
        !charaPersonality ||
        !panel
    ) return;

    // 🔹 アイコンクリック → パネル表示切替
    triggerIcon.addEventListener("click", () => {
        panel.classList.toggle("hidden");
    });

    // 🔹 テーマ選択処理
    document.querySelectorAll(".bg-card").forEach(card => {
        card.addEventListener("click", () => {

            const bg = card.dataset.bg;
            const chara = card.dataset.chara;
            const name = card.dataset.name;
            const personality = card.dataset.personality;
            const themeId = card.id; // Forest / ice など

            // 背景・キャラ画像変更
            bgImg.src = bg;
            charaImg.src = chara;

            // 名前・説明文変更
            charaName.textContent = name;
            charaPersonality.textContent = personality;

            // ★ ここが今回の本題：idをそのままclassにする
            charaName.className = `character-name ${themeId}`;
            charaPersonality.className = `character-personality ${themeId}`;

            // 🌍 グローバルに公開
            window.currentThemeId = themeId;

            // キャラごとの微調整（必要なものだけ）
            if (window.currentThemeId === "ice") {
                charaImg.style.maxHeight = "550px";
                charaImg.style.maxWidth = "550px";
            } else if (window.currentThemeId === "flame") {
                charaImg.style.maxHeight = "700px";
                charaImg.style.maxWidth = "700px";
            } else {
                charaImg.style.maxHeight = "";
                charaImg.style.maxWidth = "";
            }

            // // 状態保存（将来の復元用）
            // localStorage.setItem(
            //     "themeSet",
            //     JSON.stringify({
            //         bg,
            //         chara,
            //         name,
            //         personality,
            //         themeId
            //     })
            // );

            // パネルを閉じる
            panel.classList.add("hidden");
        });
    });
});
