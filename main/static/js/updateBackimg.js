document.addEventListener("DOMContentLoaded", () => {

    const bgBtn = document.getElementById("bgChangeBtn");
    const bgInput = document.getElementById("bgFileInput");
    const bgImage = document.querySelector(".right-back");

    /* ▼▼ ページ読み込み時：LocalStorage に保存された背景を反映 ▼▼ */
    const savedBg = localStorage.getItem("customBackground");
    if (savedBg) {
        bgImage.src = savedBg;
    }

    /* ▼▼ 背景変更ボタンを押したらファイル選択 ▼▼ */
    bgBtn.addEventListener("click", () => {
        bgInput.click();
    });

    /* ▼▼ ファイル選択後に背景変更＆保存 ▼▼ */
    bgInput.addEventListener("change", () => {
        const file = bgInput.files[0];
        if (!file) return;

        const reader = new FileReader();

        reader.onload = function (e) {
            const imageURL = e.target.result; // base64 のURL

            // 背景の画像を差し替え
            bgImage.src = imageURL;

            // LocalStorage に保存
            localStorage.setItem("customBackground", imageURL);

            console.log("背景画像を保存しました");
        };

        reader.readAsDataURL(file);
    });

});
