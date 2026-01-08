document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("deleteHistoryBtn");
    if (!btn) return;

    btn.addEventListener("click", () => {
        fetch("/run/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then(res => res.json())
        .then(() => {
            alert("履歴を削除しました");
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
