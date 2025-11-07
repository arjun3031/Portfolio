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

const skillProficiency = document.getElementById('skillProficiency');
const proficiencyValue = document.getElementById('proficiencyValue');

if (skillProficiency && proficiencyValue) {
    skillProficiency.addEventListener('input', function() {
        proficiencyValue.textContent = this.value;
    });
}

const editSkillProficiency = document.getElementById('editSkillProficiency');
const editProficiencyValue = document.getElementById('editProficiencyValue');

if (editSkillProficiency && editProficiencyValue) {
    editSkillProficiency.addEventListener('input', function() {
        editProficiencyValue.textContent = this.value;
    });
}

const editSkillModal = document.getElementById('editSkillModal');
if (editSkillModal) {
    editSkillModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        
        const skillId = button.getAttribute('data-id');
        const skillName = button.getAttribute('data-name');
        const skillCategory = button.getAttribute('data-category');
        const skillProficiency = button.getAttribute('data-proficiency');
        const skillIcon = button.getAttribute('data-icon');
        const skillDescription = button.getAttribute('data-description');
        
        document.getElementById('editSkillId').value = skillId;
        document.getElementById('editSkillName').value = skillName;
        document.getElementById('editSkillCategory').value = skillCategory;
        document.getElementById('editSkillProficiency').value = skillProficiency;
        document.getElementById('editProficiencyValue').textContent = skillProficiency;
        document.getElementById('editSkillIcon').value = skillIcon;
        document.getElementById('editSkillDescription').value = skillDescription || '';
    });
}

const deleteSkillModal = document.getElementById('deleteSkillModal');
if (deleteSkillModal) {
    deleteSkillModal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        
        const skillId = button.getAttribute('data-id');
        const skillName = button.getAttribute('data-name');
        
        document.getElementById('deleteSkillId').value = skillId;
        document.getElementById('deleteSkillName').textContent = skillName;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

const addSkillModal = document.getElementById('addSkillModal');
if (addSkillModal) {
    addSkillModal.addEventListener('hidden.bs.modal', function() {
        const form = this.querySelector('form');
        if (form) {
            form.reset();
            if (proficiencyValue) {
                proficiencyValue.textContent = '50';
            }
            if (skillProficiency) {
                skillProficiency.value = 50;
            }
        }
    });
}

document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    });
});

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