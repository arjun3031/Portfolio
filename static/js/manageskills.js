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

// Proficiency slider for Add Skill Modal
const skillProficiency = document.getElementById('skillProficiency');
const proficiencyValue = document.getElementById('proficiencyValue');

if (skillProficiency && proficiencyValue) {
    skillProficiency.addEventListener('input', function() {
        proficiencyValue.textContent = this.value;
    });
}

// Proficiency slider for Edit Skill Modal
const editSkillProficiency = document.getElementById('editSkillProficiency');
const editProficiencyValue = document.getElementById('editProficiencyValue');

if (editSkillProficiency && editProficiencyValue) {
    editSkillProficiency.addEventListener('input', function() {
        editProficiencyValue.textContent = this.value;
    });
}

// Populate Edit Modal with skill data
const editSkillModal = document.getElementById('editSkillModal');
if (editSkillModal) {
    editSkillModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        
        // Get data from button attributes
        const skillId = button.getAttribute('data-id');
        const skillName = button.getAttribute('data-name');
        const skillCategory = button.getAttribute('data-category');
        const skillProficiency = button.getAttribute('data-proficiency');
        const skillIcon = button.getAttribute('data-icon');
        const skillDescription = button.getAttribute('data-description');
        
        // Populate form fields
        document.getElementById('editSkillId').value = skillId;
        document.getElementById('editSkillName').value = skillName;
        document.getElementById('editSkillCategory').value = skillCategory;
        document.getElementById('editSkillProficiency').value = skillProficiency;
        document.getElementById('editProficiencyValue').textContent = skillProficiency;
        document.getElementById('editSkillIcon').value = skillIcon;
        document.getElementById('editSkillDescription').value = skillDescription || '';
    });
}

// Populate Delete Modal with skill data
const deleteSkillModal = document.getElementById('deleteSkillModal');
if (deleteSkillModal) {
    deleteSkillModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        
        // Get data from button attributes
        const skillId = button.getAttribute('data-id');
        const skillName = button.getAttribute('data-name');
        
        // Populate hidden input and display name
        document.getElementById('deleteSkillId').value = skillId;
        document.getElementById('deleteSkillName').textContent = skillName;
    });
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

// Reset Add Skill form when modal is closed
const addSkillModal = document.getElementById('addSkillModal');
if (addSkillModal) {
    addSkillModal.addEventListener('hidden.bs.modal', function() {
        const form = this.querySelector('form');
        if (form) {
            form.reset();
            // Reset proficiency display
            if (proficiencyValue) {
                proficiencyValue.textContent = '50';
            }
            if (skillProficiency) {
                skillProficiency.value = 50;
            }
        }
    });
}

// Form validation
document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

// Smooth scroll for better UX
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});