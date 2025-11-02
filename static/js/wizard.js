let uploadedAudio = [];
let uploadedArtwork = null;
let currentTrack = null;
let releaseData = {};

document.getElementById('audioFiles').addEventListener('change', (e) => {
    uploadedAudio = Array.from(e.target.files);
    displayAudioList();
});

document.getElementById('artworkFile').addEventListener('change', (e) => {
    uploadedArtwork = e.target.files[0];
    displayArtworkPreview();
});

function displayAudioList() {
    const list = document.getElementById('audioList');
    list.innerHTML = '<h4>Selected Tracks:</h4>';
    uploadedAudio.forEach((file, i) => {
        list.innerHTML += `<div>${i + 1}. ${file.name}</div>`;
    });
}

function displayArtworkPreview() {
    const preview = document.getElementById('artworkPreview');
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" style="max-width: 300px; border-radius: 10px;">`;
    };
    reader.readAsDataURL(uploadedArtwork);
}

function processFiles() {
    if (uploadedAudio.length === 0) {
        alert('Please select audio files');
        return;
    }
    
    const trackList = document.getElementById('trackList');
    trackList.innerHTML = '<h3>Tracks</h3>';
    
    uploadedAudio.forEach((file, i) => {
        const div = document.createElement('div');
        div.className = 'track-item';
        div.innerHTML = `
            <strong>Track ${i + 1}: ${file.name}</strong>
            <button class="btn-secondary" onclick="editTrackMetadata(${i})">Edit Metadata</button>
        `;
        trackList.appendChild(div);
    });
    
    if (uploadedArtwork) {
        const reader = new FileReader();
        reader.onload = (e) => {
            trackList.innerHTML += `<img src="${e.target.result}" style="max-width: 200px; margin-top: 20px; border-radius: 10px;">`;
        };
        reader.readAsDataURL(uploadedArtwork);
    }
    
    goToPhase(2);
}

function goToPhase(phase) {
    document.querySelectorAll('.wizard-phase').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    
    document.getElementById(`phase${phase}`).classList.add('active');
    document.querySelector(`.step[data-step="${phase}"]`).classList.add('active');
}

function handleArtistChange() {
    const select = document.getElementById('artistProfile');
    const newForm = document.getElementById('newArtistForm');
    newForm.style.display = select.value === 'new' ? 'block' : 'none';
}

function editTrackMetadata(index) {
    currentTrack = index;
    document.getElementById('trackMetadataModal').style.display = 'flex';
}

function closeTrackModal() {
    document.getElementById('trackMetadataModal').style.display = 'none';
}

function saveTrackMetadata() {
    if (!releaseData.tracks) releaseData.tracks = [];
    
    releaseData.tracks[currentTrack] = {
        isrc: document.getElementById('trackIsrc').value,
        composer: document.getElementById('composer').value,
        author: document.getElementById('author').value,
        producer: document.getElementById('producer').value,
        timecode: document.getElementById('timecode').value,
        lyrics: document.getElementById('lyrics').value,
        masteringEngineer: document.getElementById('masteringEngineer').value,
        mixingEngineer: document.getElementById('mixingEngineer').value
    };
    
    closeTrackModal();
    alert('Track metadata saved');
}

function saveAndContinue(nextPhase) {
    if (nextPhase === 3) {
        releaseData.artist = document.getElementById('artistProfile').value;
        releaseData.label = document.getElementById('labelSelect').value;
        releaseData.title = document.getElementById('releaseTitle').value;
        releaseData.upc = document.getElementById('upc').value;
        releaseData.mainGenre = document.getElementById('mainGenre').value;
        releaseData.subGenre = document.getElementById('subGenre').value;
    }
    
    goToPhase(nextPhase);
}

function toggleWorldwide(checkbox) {
    const checkboxes = document.querySelectorAll('.territory-grid input[type="checkbox"]');
    checkboxes.forEach(cb => {
        if (cb !== checkbox) cb.checked = checkbox.checked;
    });
}

document.getElementById('enablePreorder').addEventListener('change', (e) => {
    document.getElementById('preorderDate').style.display = e.target.checked ? 'block' : 'none';
});

document.getElementById('enableInstantGrat').addEventListener('change', (e) => {
    const select = document.getElementById('instantGratTrack');
    if (e.target.checked) {
        select.style.display = 'block';
        select.innerHTML = uploadedAudio.map((f, i) => `<option value="${i}">${f.name}</option>`).join('');
    } else {
        select.style.display = 'none';
    }
});

async function submitRelease() {
    const formData = new FormData();
    
    uploadedAudio.forEach((file, i) => {
        formData.append('audio', file);
    });
    
    if (uploadedArtwork) {
        formData.append('artwork', uploadedArtwork);
    }
    
    formData.append('releaseData', JSON.stringify(releaseData));
    
    try {
        const response = await fetch('/api/releases', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            alert('Release submitted successfully!');
            window.location.href = '/dashboard';
        } else {
            alert('Submission failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
