        // Typing Animation
        const texts = ['Software Engineer', 'Full Stack Developer', 'Problem Solver', 'Tech Enthusiast'];
        let textIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typingElement = document.getElementById('typingText');

        function type() {
            const currentText = texts[textIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentText.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentText.substring(0, charIndex + 1);
                charIndex++;
            }

            if (!isDeleting && charIndex === currentText.length) {
                isDeleting = true;
                setTimeout(type, 2000);
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                textIndex = (textIndex + 1) % texts.length;
                setTimeout(type, 500);
            } else {
                setTimeout(type, isDeleting ? 50 : 100);
            }
        }

        setTimeout(type, 1000);

        // Smooth Scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    // Close mobile menu if open
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse.classList.contains('show')) {
                        navbarCollapse.classList.remove('show');
                    }
                }
            });
        });

        // Fade In Animation on Scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -100px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.fade-in').forEach(element => {
            observer.observe(element);
        });

        // Progress Bar Animation
        const progressObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressBars = entry.target.querySelectorAll('.progress-bar');
                    progressBars.forEach(bar => {
                        const width = bar.getAttribute('data-width');
                        bar.style.width = width + '%';
                    });
                }
            });
        }, { threshold: 0.5 });

        const skillsSection = document.querySelector('#skills');
        if (skillsSection) {
            progressObserver.observe(skillsSection);
        }

        // Back to Top Button
        const backToTopButton = document.getElementById('backToTop');

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });

        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        document.getElementById("contactForm").addEventListener("submit", function(e) {
            e.preventDefault(); // prevent default form submission
            let isValid = true;

            // Clear previous messages
            document.getElementById("nameError").innerText = "";
            document.getElementById("emailError").innerText = "";
            document.getElementById("messageError").innerText = "";
            document.getElementById("formMessage").innerText = "";

            // Name validation (no special chars)
            let name = document.getElementById("name").value.trim();
            if (!/^[a-zA-Z\s]+$/.test(name)) {
                document.getElementById("nameError").innerText = "Name can contain only letters and spaces";
                isValid = false;
            }

            // Email validation
            let email = document.getElementById("email").value.trim();
            let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                document.getElementById("emailError").innerText = "Enter a valid email address";
                isValid = false;
            }

            // Message validation (max 1000 words)
            let message = document.getElementById("message").value.trim();
            let wordCount = message.split(/\s+/).filter(Boolean).length;
            if (wordCount > 1000) {
                document.getElementById("messageError").innerText = "Message cannot exceed 1000 words";
                isValid = false;
            }

            if (isValid) {
                // Submit via AJAX to Django view
                fetch("", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ name, email, message })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success") {
                        document.getElementById("formMessage").innerText = "Thank you! We will get back to you soon.";
                        document.getElementById("contactForm").reset();
                    } else {
                        document.getElementById("formMessage").innerText = "Something went wrong. Please try again.";
                        document.getElementById("formMessage").classList.remove("text-success");
                        document.getElementById("formMessage").classList.add("text-danger");
                    }
                })
                .catch(err => {
                    document.getElementById("formMessage").innerText = "Something went wrong. Please try again.";
                    document.getElementById("formMessage").classList.remove("text-success");
                    document.getElementById("formMessage").classList.add("text-danger");
                });
            }
        });

        // Navbar Background on Scroll
        window.addEventListener('scroll', function() {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(10, 25, 47, 0.98)';
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.3)';
            } else {
                navbar.style.background = 'rgba(10, 25, 47, 0.95)';
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.1)';
            }
        });

        // AI Chatbot Functionality
        const chatButton = document.getElementById('chatButton');
        const chatContainer = document.getElementById('chatContainer');
        const chatCloseBtn = document.getElementById('chatCloseBtn');
        const chatInput = document.getElementById('chatInput');
        const chatSendBtn = document.getElementById('chatSendBtn');
        const chatMessages = document.getElementById('chatMessages');
        const typingIndicator = document.getElementById('typingIndicator');

        // Knowledge Base
        const knowledgeBase = {
            skills: {
                keywords: ['skill', 'technology', 'tech stack', 'programming', 'languages', 'frameworks'],
                response: "Arjun is proficient in multiple technologies including:\n\n🐍 Python & Java for backend development\n💻 JavaScript, React, Node.js for full-stack development\n🗄️ SQL & NoSQL databases\n🐳 Docker for containerization\n📦 Git & GitHub for version control\n\nHe has 90% proficiency in Python and Git, 88% in JavaScript, and strong skills across the entire stack!"
            },
            experience: {
                keywords: ['experience', 'work', 'job', 'company', 'career', 'employment'],
                response: "Arjun has impressive professional experience:\n\n🏢 Currently working as a Software Engineer at MACOM Solutions (2023-Present)\n- Leading enterprise application development\n- Achieved 40% performance improvement\n- Working Under JusSuit Department - Legal tracking on notice management and case management\n\n🏢 Previously at ALTOS Technologies\n- Built responsive web applications\n- Integrated third-party APIs\n- Worked in agile environment"
            },
            projects: {
                keywords: ['project', 'built', 'created', 'developed', 'portfolio'],
                response: "Arjun has worked on several impressive projects:\n\n🎤 VocaVerse - AI-powered voice synthesis platform with 20+ languages\n\n🔍 Automated Face Sketch Identification - Deep learning system with 85% accuracy\n\n📝 Question Paper Generator - Intelligent system deployed in 5+ institutions\n\nClick on the projects in the portfolio to see more details!"
            },
            education: {
                keywords: ['education', 'degree', 'study', 'college', 'university', 'qualification'],
                response: "Arjun's educational background:\n\n🎓 Master of Computer Applications (MCA)\n2019-2021 | Specialized in Software Engineering\n\n🎓 B.Sc. Computer Science\n2016-2019 | Graduated with distinction"
            },
            contact: {
                keywords: ['contact', 'email', 'phone', 'reach', 'hire', 'connect'],
                response: "You can reach Arjun through:\n\n📧 Email: arjunkmvat@gmail.com\n📱 Phone: +91 6282283144\n💼 LinkedIn: linkedin.com/in/arjun-k-m-12411022b\n💻 GitHub: github.com/arjun3031\n\nFeel free to scroll down to the contact section to send a message!"
            },
            location: {
                keywords: ['location', 'where', 'based', 'live'],
                response: "Arjun is based in Calicut, Kerala, India"
            }
        };

        // Toggle Chat - Open
        chatButton.addEventListener('click', function() {
            chatContainer.classList.add('active');
            chatButton.classList.add('active');
            chatInput.focus();
            scrollToBottom();
        });

        // Toggle Chat - Close
        chatCloseBtn.addEventListener('click', function() {
            chatContainer.classList.remove('active');
            chatButton.classList.remove('active');
        });

        // Send Message
        function sendMessage() {
            const message = chatInput.value.trim();
            if (message === '') return;

            // Add user message
            addMessage(message, 'user');
            chatInput.value = '';

            // Show typing indicator
            typingIndicator.classList.add('active');
            scrollToBottom();

            // Generate bot response
            setTimeout(() => {
                const response = generateResponse(message);
                typingIndicator.classList.remove('active');
                addMessage(response, 'bot');
                scrollToBottom();
            }, 1000 + Math.random() * 1000);
        }

        chatSendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Quick Reply Function
        function sendQuickReply(message) {
            chatInput.value = message;
            sendMessage();
        }

        // Add Message to Chat
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
            
            const content = document.createElement('div');
            content.className = 'message-content';
            content.innerHTML = text.replace(/\n/g, '<br>');
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(content);
            
            chatMessages.appendChild(messageDiv);
        }

        // Generate Bot Response
        function generateResponse(message) {
            const lowerMessage = message.toLowerCase();
            
            // Check knowledge base
            for (const [category, data] of Object.entries(knowledgeBase)) {
                if (data.keywords.some(keyword => lowerMessage.includes(keyword))) {
                    return data.response;
                }
            }

            // Greeting responses
            if (lowerMessage.match(/^(hi|hello|hey|greetings)/)) {
                return "Hello! 👋 I'm here to help you learn more about Arjun. You can ask me about his skills, experience, projects, education, or how to contact him!";
            }

            // Thank you responses
            if (lowerMessage.match(/(thank|thanks)/)) {
                return "You're welcome! 😊 Is there anything else you'd like to know about Arjun?";
            }

            // Default response
            return "I can help you with information about:\n\n• Skills & Technologies\n• Work Experience\n• Projects\n• Education\n• Contact Information\n\nWhat would you like to know?";
        }

        // Password toggle
        
        function togglePassword() {
            const passwordInput = document.getElementById('password');
            const toggleIcon = document.getElementById('toggleIcon');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye');
            }
        }

        // Change Password 

         function openModal() {
            document.getElementById('modalOverlay').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            document.getElementById('modalOverlay').classList.remove('active');
            document.body.style.overflow = 'auto';
            document.getElementById('changePasswordForm').reset();
        }

        function closeModalOnOverlay(event) {
            if (event.target === event.currentTarget) {
                closeModal();
            }
        }

        function togglePassword(fieldId) {
            const input = document.getElementById(fieldId);
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
        }