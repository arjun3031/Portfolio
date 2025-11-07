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
          