document.addEventListener("DOMContentLoaded", () => {
    const bgBtn = document.getElementById("bgChangeBtn");
    const bgInput = document.getElementById("bgFileInput");
    const bgImage = document.querySelector(".right-back");

    if (!bgBtn || !bgInput || !bgImage) return;

    const savedBg = localStorage.getItem("customBackground");
    if (savedBg) {
        bgImage.src = savedBg;
    }

    bgBtn.addEventListener("click", () => {
        bgInput.click();
    });

    bgInput.addEventListener("change", () => {
        const file = bgInput.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = e => {
            bgImage.src = e.target.result;
            localStorage.setItem("customBackground", e.target.result);
        };
        reader.readAsDataURL(file);
    });
});
