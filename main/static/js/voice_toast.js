window.showToast = function (message, duration = 3000) {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.textContent = message;
  
    document.body.appendChild(toast);
  
    // 表示
    requestAnimationFrame(() => {
      toast.classList.add("show");
    });
  
    // 自動で消す
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, duration);
  };
  