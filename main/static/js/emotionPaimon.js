(() => {
const icon = document.getElementById("icon");
    if (!icon) {
        console.warn("⚠ 画像変更関連DOMが見つかりません", {
        icon
        });
        return;
    }

    // 感情ごとの画像
    const faceMap = {
        happy: "/static/img/ForestPaimonHappy.png", //喜び
        angry: "/static/img/ForestPaimonAnger.png", //怒り
        sad:   "/static/img/ForestPaimonSad.png", //悲しみ
        fun:   "/static/img/ForestPaimonFun.png", //楽しみ
    };

    //座標で喜怒哀楽を判定
    function judgeEmotion(x, y) {
        if (x >= 0 && y >= 0) return "happy"; // 喜
        if (x <  0 && y >= 0) return "sad";   // 哀
        if (x <  0 && y <  0) return "angry"; // 怒
        return "fun";                         // 楽
    }

    //外部から呼べる関数
    window.updateFaceByEmotion = function (x, y) {
        const type = judgeEmotion(x, y);
        const newSrc = faceMap[type];

        // 既に同じ画像なら変更しない
        if (icon.src.includes(newSrc)) return;

        icon.src = newSrc;
    };
})();