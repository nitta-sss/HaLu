document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       emotion 初期化（安全対策）
    ========================= */
    if (!window.emotion) {
        window.emotion = { x: 0, y: 0 };
    }

    const awakeBar   = document.getElementById("awakeBar");
    const pleasureBar = document.getElementById("pleasureBar");
    const gauge      = document.getElementById("emotionArea");
    const btn        = document.getElementById("showbtn");

    // 必須要素が無ければ何もしない（エラー防止）
    if (!awakeBar || !pleasureBar || !gauge || !btn) {
        console.warn("⚠ ゲージ関連DOMが見つかりません");
        return;
    }

    /* =========================
       数値正規化
    ========================= */
    function normalize(v) {
        // -1 ～ +1 → 0 ～ 100
        return Math.max(0, Math.min(100, (v + 1) * 50));
    }

    /* =========================
       ゲージ描画
    ========================= */
    function updateGauge() {
        const awake    = normalize(window.emotion.x);
        const pleasure = normalize(window.emotion.y);

        // 幅
        awakeBar.style.width = awake + "%";
        pleasureBar.style.width = pleasure + "%";

        // 覚醒度（青 → 赤）
        const r = Math.round(awake * 2.55);
        const b = Math.round(255 - awake * 2.55);
        awakeBar.style.background =
            `linear-gradient(to right, rgb(${r},0,${b}), rgba(255,255,255,0.6))`;

        // 快楽度（赤 → 黄）
        if (pleasure < 30) {
            pleasureBar.style.background =
                "linear-gradient(to right, red, orange)";
        } else if (pleasure < 70) {
            pleasureBar.style.background =
                "linear-gradient(to right, orange, yellow)";
        } else {
            pleasureBar.style.background =
                "linear-gradient(to right, yellow, lightyellow)";
        }
    }

    /* =========================
       初期状態
    ========================= */
    updateGauge();                 // 値は描画
    gauge.classList.add("hide");   // でも非表示
    btn.textContent = "ゲージ表示";

    /* =========================
       表示切り替え
    ========================= */
    btn.addEventListener("click", () => {
        gauge.classList.toggle("hide");
        btn.textContent = gauge.classList.contains("hide")
            ? "ゲージ表示"
            : "ゲージ非表示";
    });

    /* =========================
       外部更新用（任意）
       他JSから window.updateEmotion(x,y) で更新可能
    ========================= */
    window.updateEmotion = (x, y) => {
        window.emotion.x = x;
        window.emotion.y = y;
        updateGauge();
    };
});
