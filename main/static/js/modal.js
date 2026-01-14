window.showErrorModal = function (message) {
    const modal = document.getElementById("errorModal");
    const text = document.getElementById("modalMessage");
  
    if (!modal || !text) return;
  
    text.textContent = message;
    modal.classList.remove("hidden");
  };
  
  document.addEventListener("DOMContentLoaded", () => {
    const okBtn = document.getElementById("modalOk");
    if (!okBtn) return;
  
    okBtn.addEventListener("click", () => {
      document.getElementById("errorModal")?.classList.add("hidden");
    });
  });