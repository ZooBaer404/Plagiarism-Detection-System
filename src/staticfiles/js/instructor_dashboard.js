document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const fileDetails = document.getElementById("fileDetails");
  const generateBtn = document.getElementById("generateBtn");

  // Hide until file is selected
  fileDetails.classList.add("hidden");
  generateBtn.classList.add("hidden");

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      fileDetails.textContent = `${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
      fileDetails.classList.remove("hidden");
      generateBtn.classList.remove("hidden");
    } else {
      fileDetails.classList.add("hidden");
      generateBtn.classList.add("hidden");
    }
  });

  // generateBtn.addEventListener("click", () => {
  //   generateBtn.textContent = "Generating…";
  //   generateBtn.classList.add("processing");

  //   setTimeout(() => {
  //     window.location.href = "/dashboard/instructor/report_preview/";
  //   }, 2000);
  // });
});
