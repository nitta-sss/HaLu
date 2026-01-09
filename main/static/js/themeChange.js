document.addEventListener("DOMContentLoaded", () => {

    // 🔹 トリガー：左上アイコン
    const triggerIcon = document.querySelector(".icon");

    // 🔹 変更対象
    const bgImg = document.querySelector(".right-back");
    const charaImg = document.getElementById("icon"); // 右側HaLu

    // 🔹 選択パネル
    const panel = document.getElementById("bgSelectPanel");

    if (!triggerIcon || !bgImg || !charaImg || !panel) return;

    // // 保存済みテーマ復元
    // const savedTheme = JSON.parse(localStorage.getItem("themeSet"));
    // if (savedTheme) {
    //     bgImg.src = savedTheme.bg;
    //     charaImg.src = savedTheme.chara;
    // }

    // アイコンクリック → パネル表示
    triggerIcon.addEventListener("click", () => {
        panel.classList.toggle("hidden");
    });

    // テーマ選択
    document.querySelectorAll(".bg-card").forEach(card => {
        card.addEventListener("click", () => {
            const bg = card.dataset.bg;
            const chara = card.dataset.chara;

            bgImg.src = bg;
            charaImg.src = chara;

            if(card.id === "ice") {
                charaImg.style.maxHeight = "550px";
                charaImg.style.maxWidth = "550px";
            }

            localStorage.setItem(
                "themeSet",
                JSON.stringify({ bg, chara })
            );

            panel.classList.add("hidden");
        });
    });
});
