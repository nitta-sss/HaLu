const sendinput = document.getElementById("textInput");
const sendbtn = document.getElementById("sendBtn");

console.log(sendinput, sendbtn); 

sendinput.addEventListener("input", () => {
    if (sendinput.value.trim() !== "") {
        sendbtn.classList.add("active");
    } else {
        sendbtn.classList.remove("active");
    }
});
