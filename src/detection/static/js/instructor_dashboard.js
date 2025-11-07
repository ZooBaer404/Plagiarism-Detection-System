document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  const generateBtn = document.getElementById("generateBtn");
  const fileDetails = document.getElementById("fileDetails");

  if (!fileInput || !generateBtn) return;

  // Hide button initially
  generateBtn.style.display = "none";

  // When file selected
  fileInput.addEventListener("change", function () {
    if (fileInput.files && fileInput.files.length > 0) {
      const file = fileInput.files[0];

      // ✅ Show file name
      if (fileDetails) {
        fileDetails.textContent = `Selected: ${file.name}`;
        fileDetails.classList.remove("hidden");
      }

      // ✅ Show generate button
      generateBtn.style.display = "inline-block";
    } else {
      generateBtn.style.display = "none";
      if (fileDetails) fileDetails.classList.add("hidden");
    }
  });

  // ✅ When user clicks "Generate Report"
  generateBtn.addEventListener("click", function () {
    // Optional: add small delay or animation
    setTimeout(() => {
      window.location.href = "/dashboard/instructor/report/"; 
      // 🔹 Change this path if your route name differs
    }, 300);
  });
});
