// document.addEventListener("DOMContentLoaded", () => {

//     // 要素の取得
//     const bgBtn = document.getElementById("bgChangeBtn");   // 背景変更ボタン
//     const bgInput = document.getElementById("bgFileInput"); // ファイル選択input
//     const bgTarget = document.querySelector(".right-back"); // 背景を変えたい要素

//     // 許可する画像拡張子
//     const allowedExtensions = ["jpg", "jpeg", "png", "webp"];

//     // ボタン → ファイル選択を開く
//     bgBtn.addEventListener("click", () => {
//         bgInput.click(); // input[type=file] を擬似クリック
//     });

//     // ファイルが選ばれたとき
//     bgInput.addEventListener("change", () => {

//         // 選択されたファイルを取得
//         const file = bgInput.files[0];

//         // キャンセルされた場合
//         if (!file) return;

//         // 拡張子チェック

//         // ファイル名から拡張子を取得
//         const fileName = file.name;
//         const extension = fileName.split(".").pop().toLowerCase();

//         // 許可されていない拡張子だった場合
//         if (!allowedExtensions.includes(extension)) {
//             alert("画像ファイルのみ選択できます");

//             // ファイル選択をリセット
//             bgInput.value = "";
//             return;
//         }

//         // 背景画像を変更 

//         // 一時URLを生成
//         const imageURL = URL.createObjectURL(file);

//         // 背景画像として設定
//         bgTarget.src = imageURL;

//         // LocalStorage に保存
//         localStorage.setItem("bgImage", imageURL);
//     });

// });
