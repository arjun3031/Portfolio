const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

mobileMenuToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
    sidebarOverlay.classList.toggle('active');
    
    const icon = this.querySelector('i');
    if (sidebar.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

sidebarOverlay.addEventListener('click', function() {
    sidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    const icon = mobileMenuToggle.querySelector('i');
    icon.classList.remove('fa-times');
    icon.classList.add('fa-bars');
});

const navLinks = document.querySelectorAll('.sidebar .nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });
});

const adminAvatar = document.getElementById('adminAvatar');
const profileDropdown = document.getElementById('profileDropdown');

adminAvatar.addEventListener('click', function(e) {
    e.stopPropagation();
    profileDropdown.classList.toggle('active');
});

document.addEventListener('click', function(e) {
    if (!adminAvatar.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('active');
    }
});

const dropdownItems = document.querySelectorAll('.dropdown-item-custom');
dropdownItems.forEach(item => {
    item.addEventListener('click', function() {
        profileDropdown.classList.remove('active');
    });
});

window.addEventListener('load', () => {
    document.querySelectorAll('.progress-bar').forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var changeModalEl = document.getElementById('changePasswordModal');
    var changeModal = new bootstrap.Modal(changeModalEl);

    const urlParams = new URLSearchParams(window.location.search);
    const modal = urlParams.get('modal');

    if (modal === 'change') {
        changeModal.show();
    }

    changeModalEl.addEventListener('hidden.bs.modal', function () {
        var alerts = changeModalEl.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove());
        var form = document.getElementById('changePasswordForm');
        if (form) form.reset();
    });

    var forgotModalEl = document.getElementById('forgotPasswordModal');
    forgotModalEl.addEventListener('hidden.bs.modal', function () {
        var form = document.getElementById('forgotPasswordForm');
        if (form) form.reset();
    });
});

let currentEnquiryId = null;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function viewEnquiry(enquiryId) {
    currentEnquiryId = enquiryId;
    const detailModal = new bootstrap.Modal(document.getElementById('enquiryDetailModal'));
    detailModal.show();

    fetch(`/adminhome/enquiry/${enquiryId}/`, {
    method: 'GET',
    headers: {
        'X-CSRFToken': csrftoken
     }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const enquiry = data.enquiry;
            document.getElementById('enquiryDetailContent').innerHTML = `
                <div class="mb-3">
                    <label class="form-label fw-bold">Name:</label>
                    <p class="form-control-plaintext">${enquiry.name}</p>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Email:</label>
                    <p class="form-control-plaintext">
                        <a href="mailto:${enquiry.email}" class="text-decoration-none" style="color: var(--accent-color);">
                            ${enquiry.email}
                        </a>
                    </p>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">Message:</label>
                    <p class="form-control-plaintext" style="white-space: pre-wrap;">${enquiry.message}</p>
                </div>
                <div class="mb-0">
                    <label class="form-label fw-bold">Received:</label>
                    <p class="form-control-plaintext text-muted">${enquiry.created_at}</p>
                </div>
            `;

            updateUnreadCount(data.unread_count);

            const enquiryItem = document.querySelector(`[data-enquiry-id="${enquiryId}"]`);
            if (enquiryItem) {
                enquiryItem.classList.remove('unread');
                const badge = enquiryItem.querySelector('.badge');
                if (badge) badge.remove();
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('enquiryDetailContent').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>Failed to load enquiry details
            </div>
        `;
    });
}

function deleteEnquiry() {
    if (!currentEnquiryId) {
        console.error('No enquiry ID set');
        alert('No enquiry selected');
        return;
    }

    if (!confirm('Are you sure you want to delete this enquiry?')) return;

    const csrftoken = getCookie('csrftoken');
    
    console.log('=== DELETE DEBUG ===');
    console.log('Enquiry ID:', currentEnquiryId);
    console.log('CSRF Token:', csrftoken);
    console.log('URL:', `/adminhome/enquiry/${currentEnquiryId}/delete/`);
    
    if (!csrftoken) {
        alert('Security token missing. Please refresh the page.');
        return;
    }

    fetch(`/adminhome/enquiry/${currentEnquiryId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Response Status:', response.status);
        console.log('Response OK:', response.ok);
        console.log('Response Headers:', [...response.headers.entries()]);
        
        return response.text().then(text => {
            console.log('Raw Response:', text);
            
            try {
                const data = JSON.parse(text);
                return { status: response.status, ok: response.ok, data: data };
            } catch (e) {
                console.error('Failed to parse JSON:', e);
                throw new Error(`Server returned invalid JSON. Status: ${response.status}, Response: ${text.substring(0, 200)}`);
            }
        });
    })
    .then(({ status, ok, data }) => {
        console.log('Parsed Data:', data);
        
        if (data.status === 'success') {
            console.log('✓ Delete successful');
            
            bootstrap.Modal.getInstance(document.getElementById('enquiryDetailModal')).hide();

            const enquiryItem = document.querySelector(`[data-enquiry-id="${currentEnquiryId}"]`);
            if (enquiryItem) {
                enquiryItem.remove();
            }

            updateUnreadCount(data.unread_count);
            document.getElementById('totalEnquiries').textContent = data.total_count;

            const enquiriesList = document.getElementById('enquiriesList');
            if (enquiriesList.children.length === 0) {
                enquiriesList.innerHTML = `
                    <div class="text-center py-5">
                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                        <p class="text-muted">No enquiries yet</p>
                    </div>
                `;
            }
            
            alert('Enquiry deleted successfully!');
        } else {
            console.error('✗ Delete failed:', data.message);
            alert(data.message || 'Failed to delete enquiry');
        }
    })
    .catch(error => {
        console.error('=== ERROR ===');
        console.error('Error Type:', error.name);
        console.error('Error Message:', error.message);
        console.error('Full Error:', error);
        alert('Failed to delete enquiry: ' + error.message);
    });
}


function updateUnreadCount(count) {
    const topBarBadge = document.getElementById('topBarBadge');
    const modalBadge = document.getElementById('modalBadge');

    if (count > 0) {
        if (topBarBadge) {
            topBarBadge.textContent = count;
            topBarBadge.style.display = 'inline-block';
        } else {
            const btn = document.querySelector('[data-bs-target="#enquiriesModal"]');
            btn.insertAdjacentHTML('beforeend', `<span class="notification-badge" id="topBarBadge">${count}</span>`);
        }

        if (modalBadge) {
            modalBadge.textContent = count + ' New';
        }
    } else {
        if (topBarBadge) topBarBadge.remove();
        if (modalBadge) modalBadge.remove();
    }
}