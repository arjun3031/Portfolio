        // document.querySelectorAll('.nav-link').forEach(link => {
        //     link.addEventListener('click', function(e) {
        //         const href = this.getAttribute('href');

        //         if (!href || href === '#' || href === '') {
        //             e.preventDefault();
        //         } else {
        //             window.location.href = href;
        //         }

        //         document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        //         this.classList.add('active');
        //     });
        // });


        window.addEventListener('load', () => {
            document.querySelectorAll('.progress-bar').forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        });