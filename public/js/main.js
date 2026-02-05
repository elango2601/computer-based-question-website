const API_BASE = '/api';

// Utilities
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerText = message;
    document.body.appendChild(toast);

    // Trigger reflow
    toast.offsetHeight;

    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await res.json();

        // Handle unauthorized globally
        if (res.status === 401 && !endpoint.includes('login') && !endpoint.includes('register')) {
            const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';
            if (!isIndex) {
                window.location.href = '/index.html';
                return;
            }
        }

        return { status: res.status, data };
    } catch (err) {
        showToast('Network error', 'error');
        console.error(err);
        return { status: 500, data: { error: 'Network error' } };
    }
}

function checkAuth(roleReq = null) {
    apiCall('/me').then(({ status, data }) => {
        if (status !== 200) {
            window.location.href = '/index.html';
        } else {
            if (roleReq && data.role !== roleReq) {
                window.location.href = data.role === 'admin' ? '/admin.html' : '/dashboard.html';
            }
            // Update UI with user info if element exists
            const userDisplay = document.getElementById('user-display');
            if (userDisplay) userDisplay.textContent = `Hello, ${data.username}`;
        }
    });
}

function logout() {
    apiCall('/logout', 'POST').then(() => {
        window.location.href = '/index.html';
    });
}
