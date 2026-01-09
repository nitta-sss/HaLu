document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("deleteHistoryBtn");
    if (!btn) return;

    btn.addEventListener("click", () => {

        // ★ 最終確認ダイアログ
        const ok = confirm("本当に会話履歴を削除しますか？\nこの操作は元に戻せません。");

        if (!ok) {
            return; // キャンセルされたら何もしない
        }

        fetch("/run/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then(res => res.json())
        .then(() => {
            alert("履歴を削除しました");
        })
        .catch(err => {
            alert("削除に失敗しました");
            console.error(err);
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    document.cookie.split(";").forEach(c => {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(c.substring(name.length + 1));
        }
    });
    return cookieValue;
}
