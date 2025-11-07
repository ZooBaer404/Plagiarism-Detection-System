document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("multiFileInput");
  const fileList = document.getElementById("fileList");
  const uploadAllBtn = document.getElementById("uploadAllBtn");
  const noFilesMsg = document.getElementById("noFilesMsg");

  let selectedFiles = [];

  // When user selects files
  fileInput.addEventListener("change", () => {
    selectedFiles = Array.from(fileInput.files);
    renderFileList();
  });

  // Render list with remove (-) button
  function renderFileList() {
    fileList.innerHTML = "";

    if (selectedFiles.length === 0) {
      fileList.classList.add("hidden");
      uploadAllBtn.classList.add("hidden");
      noFilesMsg.classList.remove("hidden");
      return;
    }

    noFilesMsg.classList.add("hidden");
    fileList.classList.remove("hidden");

    selectedFiles.forEach((file, index) => {
      const fileSize = (file.size / 1024 / 1024).toFixed(2);
      const fileRow = document.createElement("div");
      fileRow.classList.add("file-row");

      fileRow.innerHTML = `
        <span class="file-name">${file.name}</span>
        <span class="file-size">(${fileSize} MB)</span>
        <button class="remove-btn" data-index="${index}">−</button>
      `;

      fileList.appendChild(fileRow);
    });

    uploadAllBtn.classList.remove("hidden");
  }

  // Remove file
  fileList.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-btn")) {
      const index = e.target.dataset.index;
      selectedFiles.splice(index, 1);
      renderFileList();
    }
  });

  // Upload simulation
  uploadAllBtn.addEventListener("click", () => {
    uploadAllBtn.textContent = "Uploading...";
    uploadAllBtn.classList.add("uploading");


    setTimeout(() => {
      window.location.href = "/university/upload/done/";
    }, 2500);

  });
});
