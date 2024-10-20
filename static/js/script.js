const dropArea = document.getElementById('drop-area');
const fileElem = document.getElementById('fileElem');
let uploadedImage = null;

// Handle file selection
fileElem.addEventListener('change', handleFiles);
dropArea.addEventListener('drop', handleDrop, false);
dropArea.addEventListener('dragover', (e) => { e.preventDefault(); }, false);

function handleFiles(e) {
    const file = e.target.files[0];
    if (file) {
        showImage(file);
    }
}

function handleDrop(e) {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) {
        showImage(file);
    }
}

function showImage(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        uploadedImage = file;
        document.getElementById('img-display').src = e.target.result;
        document.getElementById('convert-btn').disabled = false;
    };
    reader.readAsDataURL(file);
}

// Handle conversion and fetching the processed image
document.getElementById('convert-btn').addEventListener('click', async () => {
    if (uploadedImage) {
        const formData = new FormData();
        formData.append('file', uploadedImage);
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.status === 'success') {
                document.getElementById('bw-display').src = data.bw_image_url;
                document.getElementById('download-btn').href = data.bw_image_url;
                document.getElementById('download-btn').style.display = 'inline';
            } else {
                document.getElementById('error-msg').textContent = data.error;
            }
        } catch (err) {
            document.getElementById('error-msg').textContent = 'Error processing the image.';
        }
    }
});
