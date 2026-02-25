async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const courierSelect = document.getElementById("courierSelect");
    const status = document.getElementById("status");

    if (fileInput.files.length === 0) {
        status.className = "error";
        status.innerText = "Please select a file.";
        return;
    }

    const courier = courierSelect.value;
    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    status.className = "";
    status.innerText = "Processing...";

    try {

        const response = await fetch(`http://127.0.0.1:8000/upload/${courier}`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Upload failed");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `${courier}_billing_output.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();

        status.className = "success";
        status.innerText = "File processed successfully.";

    } catch (error) {
        status.className = "error";
        status.innerText = error.message;
    }
}