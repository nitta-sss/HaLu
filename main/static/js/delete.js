document.addEventListener("DOMContentLoaded", () => {
    console.log("① DOMContentLoaded 発火");

    const btn = document.getElementById("deleteHistoryBtn");
    console.log("② deleteHistoryBtn 取得:", btn);

    if (!btn) {
        console.log("③ ボタンが無いので終了");
        return;
    }

    btn.addEventListener("click", () => {
        console.log("④ 削除ボタンがクリックされた");

        // ★ 最終確認ダイアログ
        const ok = confirm("本当に会話履歴を削除しますか？\nこの操作は元に戻せません。");
        console.log("⑤ confirm の結果:", ok);

        if (!ok) {
            console.log("⑥ キャンセルされたので終了");
            return;
        }

        console.log("⑦ fetch 開始 → /run/");

        fetch("http://127.0.0.1:5000/ai/reset", {
            method: "POST"
        })
        .then(res => {
            console.log("⑧ reset response:", res);
            return res.json();
        })
        .then(data => {
            console.log("⑨ reset result:", data);
            alert("履歴を削除しました");
        })
        .catch(err => {
            console.error("⑩ reset error", err);
            alert("削除に失敗しました");
        });
        
    });
});

function getCookie(name) {
    console.log("⑪ getCookie 呼び出し:", name);

    let cookieValue = null;
    document.cookie.split(";").forEach(c => {
        c = c.trim();
        if (c.startsWith(name + "=")) {
            cookieValue = decodeURIComponent(c.substring(name.length + 1));
            console.log("⑫ Cookie 発見:", cookieValue);
        }
    });

    if (!cookieValue) {
        console.log("⑬ Cookie が見つからなかった");
    }

    return cookieValue;
}
