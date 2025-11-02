let currentReleaseId = null;

function showReviewModal(releaseId) {
    currentReleaseId = releaseId;
    document.getElementById('reviewModal').style.display = 'flex';
}

function closeReviewModal() {
    document.getElementById('reviewModal').style.display = 'none';
    currentReleaseId = null;
}

async function approveRelease() {
    const upc = document.getElementById('upcInput').value;
    
    try {
        const response = await fetch(`/api/admin/releases/${currentReleaseId}/approve`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({upc})
        });
        
        if (response.ok) {
            alert('Release approved successfully');
            closeReviewModal();
            location.reload();
        }
    } catch (error) {
        alert('Error approving release');
    }
}

async function rejectRelease() {
    const feedback = document.getElementById('feedbackInput').value;
    
    if (!feedback) {
        alert('Please provide feedback for rejection');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/releases/${currentReleaseId}/reject`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({feedback})
        });
        
        if (response.ok) {
            alert('Release rejected and sent back to draft');
            closeReviewModal();
            location.reload();
        }
    } catch (error) {
        alert('Error rejecting release');
    }
}

async function refreshDelivery(deliveryId) {
    try {
        const response = await fetch(`/api/admin/deliveries/${deliveryId}/refresh`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Delivery refreshed successfully');
            location.reload();
        }
    } catch (error) {
        alert('Error refreshing delivery');
    }
}

function showAddStoreModal() {
    const storeName = prompt('Store Name:');
    const apiUrl = prompt('API URL:');
    const apiKey = prompt('API Key:');
    const apiSecret = prompt('API Secret (optional):');
    
    if (storeName && apiUrl && apiKey) {
        addStore({storeName, apiUrl, apiKey, apiSecret});
    }
}

async function addStore(data) {
    try {
        const response = await fetch('/api/admin/stores', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Store added successfully');
            location.reload();
        }
    } catch (error) {
        alert('Error adding store');
    }
}

function showCreateStatementModal() {
    const userId = prompt('User ID:');
    const periodStart = prompt('Period Start (YYYY-MM-DD):');
    const periodEnd = prompt('Period End (YYYY-MM-DD):');
    
    if (userId && periodStart && periodEnd) {
        createStatement({userId, periodStart, periodEnd});
    }
}

async function createStatement(data) {
    try {
        const response = await fetch('/api/admin/statements', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Statement created successfully');
            location.reload();
        }
    } catch (error) {
        alert('Error creating statement');
    }
}

function showMapArtistModal() {
    const artistName = prompt('Artist Name:');
    const userId = prompt('User ID:');
    const spotifyId = prompt('Spotify ID (optional):');
    const appleMusicId = prompt('Apple Music ID (optional):');
    const youtubeId = prompt('YouTube ID (optional):');
    
    if (artistName && userId) {
        mapArtist({artistName, userId, spotifyId, appleMusicId, youtubeId});
    }
}

async function mapArtist(data) {
    try {
        const response = await fetch('/api/admin/artists', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Artist profile mapped successfully');
            location.reload();
        }
    } catch (error) {
        alert('Error mapping artist');
    }
}

function showAddUserModal() {
    const email = prompt('Email:');
    const password = prompt('Password:');
    const fullName = prompt('Full Name:');
    const isAdmin = confirm('Make admin?') ? 1 : 0;
    
    if (email && password && fullName) {
        createUser({email, password, fullName, isAdmin});
    }
}

async function createUser(data) {
    try {
        const response = await fetch('/api/admin/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('User created');
            location.reload();
        }
    } catch (error) {
        alert('Error creating user');
    }
}

function showAddLabelModal() {
    const name = prompt('Label Name:');
    const ownerId = prompt('Owner User ID:');
    const description = prompt('Description (optional):');
    
    if (name && ownerId) {
        createLabel({name, ownerId, description});
    }
}

async function createLabel(data) {
    try {
        const response = await fetch('/api/admin/labels', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (response.ok) {
            alert('Label created');
            location.reload();
        }
    } catch (error) {
        alert('Error creating label');
    }
}

async function uploadAccountingCSV() {
    const fileInput = document.getElementById('accountingCSV');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a CSV file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/admin/accounting/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            displayAccountingResults(data.results);
        }
    } catch (error) {
        alert('Error uploading CSV');
    }
}

function displayAccountingResults(results) {
    const container = document.getElementById('accountingResults');
    let html = '<table><thead><tr><th>Artist</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
    
    results.forEach(r => {
        const status = r.assigned ? '<span style="color: #10b981;">Assigned</span>' : '<span style="color: #f59e0b;">Unassigned</span>';
        const action = r.assigned ? '' : '<button class="btn-primary" onclick="assignArtist(\'' + r.artist + '\')">Assign</button>';
        html += `<tr><td>${r.artist}</td><td>${status}</td><td>${action}</td></tr>`;
    });
    
    html += '</tbody></table>';
    container.innerHTML = html;
    container.style.display = 'block';
}

function assignArtist(artistName) {
    const userId = prompt('Enter User ID to assign artist to:');
    if (userId) {
        mapArtist({artistName, userId});
    }
}

async function updateSettings(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/api/admin/settings', {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Settings updated');
        }
    } catch (error) {
        alert('Error updating settings');
    }
}
