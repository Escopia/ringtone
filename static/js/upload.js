let uploadedFile = null;

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const validTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/aac', 'audio/flac', 'audio/ogg', 'audio/m4a'];
    if (!file.type.startsWith('audio/')) {
        alert('Please select a valid audio file');
        return;
    }
    
    uploadedFile = file;
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
    document.getElementById('fileInfo').style.display = 'block';
}

async function uploadTrack(event) {
    event.preventDefault();
    
    if (!uploadedFile) {
        alert('Please select an audio file');
        return;
    }
    
    const formData = new FormData(event.target);
    formData.append('file', uploadedFile);
    
    const progressBar = document.getElementById('uploadProgress');
    const progressContainer = document.getElementById('progressContainer');
    progressContainer.style.display = 'block';
    
    try {
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
                progressBar.textContent = Math.round(percentComplete) + '%';
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200 || xhr.status === 201) {
                alert('Track uploaded successfully!');
                event.target.reset();
                uploadedFile = null;
                document.getElementById('fileInfo').style.display = 'none';
                progressContainer.style.display = 'none';
                progressBar.style.width = '0%';
                progressBar.textContent = '0%';
            } else {
                alert('Upload failed. Please try again.');
                console.error('Upload error:', xhr.responseText);
            }
        });
        
        xhr.addEventListener('error', () => {
            alert('Network error. Please check your connection.');
        });
        
        xhr.open('POST', '/api/tracks');
        xhr.send(formData);
        
    } catch (error) {
        alert('Upload error: ' + error.message);
    }
}

function showDistributionForm() {
    document.getElementById('distributionModal').style.display = 'flex';
}

function closeDistributionForm() {
    document.getElementById('distributionModal').style.display = 'none';
}

function submitDistribution(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const stores = formData.getAll('stores');
    
    if (stores.length === 0) {
        alert('Please select at least one store');
        return;
    }
    
    alert('Distribution submitted to: ' + stores.join(', '));
    closeDistributionForm();
}
