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
