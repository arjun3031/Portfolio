// Mobile menu toggle functionality
const mobileMenuToggle = document.getElementById('mobileMenuToggle');
const sidebar = document.querySelector('.sidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// Toggle sidebar on button click
mobileMenuToggle.addEventListener('click', function() {
    sidebar.classList.toggle('active');
    sidebarOverlay.classList.toggle('active');
    
    // Toggle icon between bars and times
    const icon = this.querySelector('i');
    if (sidebar.classList.contains('active')) {
        icon.classList.remove('fa-bars');
        icon.classList.add('fa-times');
    } else {
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
    }
});

// Close sidebar when clicking overlay
sidebarOverlay.addEventListener('click', function() {
    sidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    const icon = mobileMenuToggle.querySelector('i');
    icon.classList.remove('fa-times');
    icon.classList.add('fa-bars');
});

// Close sidebar when clicking a nav link on mobile
const navLinks = document.querySelectorAll('.sidebar .nav-link');
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

// Toggle end date field based on "Currently working here" checkbox
function toggleEndDate(formType) {
    const isCurrentCheckbox = document.getElementById(formType + 'IsCurrent');
    const endDateInput = document.getElementById(formType + 'EndDate');
    
    if (isCurrentCheckbox.checked) {
        endDateInput.disabled = true;
        endDateInput.required = false;
        endDateInput.value = '';
        endDateInput.parentElement.style.opacity = '0.5';
    } else {
        endDateInput.disabled = false;
        endDateInput.required = false;
        endDateInput.parentElement.style.opacity = '1';
    }
}

// Open edit modal with pre-filled data
function openEditModal(id, companyName, jobTitle, location, startDate, endDate, isCurrent, description, technologies, order, logoUrl) {
    // Set form action
    const editForm = document.getElementById('editForm');
    editForm.action = `/update-experience/${id}/`;
    
    // Fill in the form fields
    document.getElementById('editCompanyName').value = companyName;
    document.getElementById('editJobTitle').value = jobTitle;
    document.getElementById('editLocation').value = location;
    document.getElementById('editStartDate').value = startDate;
    document.getElementById('editEndDate').value = endDate;
    document.getElementById('editIsCurrent').checked = isCurrent;
    document.getElementById('editDescription').value = description;
    document.getElementById('editTechnologies').value = technologies;
    document.getElementById('editOrder').value = order;
    
    // Handle end date field visibility
    toggleEndDate('edit');
    
    // Show current logo if exists
    if (logoUrl) {
        document.getElementById('currentLogoPreview').style.display = 'block';
        document.getElementById('currentLogoImg').src = logoUrl;
    } else {
        document.getElementById('currentLogoPreview').style.display = 'none';
    }
    
    // Show the modal
    const editModal = new bootstrap.Modal(document.getElementById('editExperienceModal'));
    editModal.show();
}

// Confirm delete
function confirmDelete(id, companyName) {
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/delete-experience/${id}/`;
    
    document.getElementById('deleteCompanyName').textContent = companyName;
    
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Auto-dismiss alerts after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});