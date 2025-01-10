document.getElementById("uploadForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const files = document.getElementById("files").files;

    if (files.length === 0) {
        alert("Please select at least one file to upload.");
        return;
    }

    const allowedExtensions = ["pdf", "doc", "docx"];
    for (let i = 0; i < files.length; i++) {
        const fileExtension = files[i].name.split(".").pop().toLowerCase();
        if (!allowedExtensions.includes(fileExtension)) {
            alert("Only PDF, DOC, and DOCX files are allowed.");
            return;
        }
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    try {
        const response = await fetch("/upload/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        console.log("Response:", data);

        const resultsDiv = document.getElementById("results");
        // resultsDiv.innerHTML = "<h2>Uploaded Files and Results:</h2>";

        // Hiển thị kết quả upload
        data.results.forEach(result => {
            const resultHTML = `
                <div>
                    <strong>File Name:</strong> ${result.file_name}<br>
                    <strong>Name:</strong> ${result.name || "N/A"}<br>
                    <strong>Skills:</strong> ${(result.skills || []).join(", ")}<br>
                    <strong>Experience:</strong> ${result.experience || "N/A"}<br>
                </div>
                <hr>
            `;
            resultsDiv.innerHTML += resultHTML;
        });

        const downloadButtonHTML = `
            <div>
                <a href="/download/${data.output_csv}" class="download-link" target="_blank">
                    <button class="download-button">Download CSV</button>
                </a>
            </div>
        `;
        resultsDiv.innerHTML += downloadButtonHTML;
    } catch (error) {
        console.error("Error uploading files:", error);
        alert("An error occurred while uploading the files.");
    }
});

// Hàm cập nhật tên file khi người dùng chọn file
function updateFileName() {
    const fileInput = document.getElementById('files');
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    // Kiểm tra nếu có file được chọn
    if (fileInput.files.length > 0) {
        // Hiển thị tên tất cả các file đã chọn
        const fileNames = Array.from(fileInput.files).map(file => file.name).join(", ");
        fileNameDisplay.textContent = `Selected Files: ${fileNames}`; // Hiển thị tên các file
    } else {
        fileNameDisplay.textContent = 'No file selected'; // Nếu không có file nào được chọn
    }
}
