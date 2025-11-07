document.addEventListener("DOMContentLoaded", () => {
  const approveButtons = document.querySelectorAll(".btn-approve");
  const rejectButtons = document.querySelectorAll(".btn-reject");

  approveButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest(".pending-card").style.background = "rgba(46,204,113,0.2)";
      btn.closest(".pending-card").querySelector(".uni-info h3").textContent += " (Approved ✅)";
    });
  });

  rejectButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      btn.closest(".pending-card").style.background = "rgba(231,76,60,0.2)";
      btn.closest(".pending-card").querySelector(".uni-info h3").textContent += " (Rejected ❌)";
    });
  });
});
