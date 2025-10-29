

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

// Contact Form Validation
document.getElementById("contactForm").addEventListener("submit", function(e) {
    e.preventDefault();
    let isValid = true;

    // Clear previous messages
    document.getElementById("nameError").innerText = "";
    document.getElementById("emailError").innerText = "";
    document.getElementById("messageError").innerText = "";
    document.getElementById("formMessage").innerText = "";

    // Name validation
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

    // Message validation
    let message = document.getElementById("message").value.trim();
    let wordCount = message.split(/\s+/).filter(Boolean).length;
    if (wordCount > 1000) {
        document.getElementById("messageError").innerText = "Message cannot exceed 1000 words";
        isValid = false;
    }

    if (isValid) {
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

// ==================== AI CHATBOT FUNCTIONALITY ====================

// Enhanced Knowledge Base
const knowledgeBase = {
    greeting: {
        keywords: ['hi', 'hello', 'hey', 'hola', 'namaste', 'greetings', 'good morning', 'good evening', 
                   'good afternoon', 'sup', 'whats up', 'howdy', 'haai', 'ooi', 'heloo', 'kooi', 'hlo'],
        response: function() {
            const greetings = [
                `Hello! 👋 I'm here to help you learn more about ${chatbotData.heroData.name}.`,
                `Hey there! 👋 Welcome! I can tell you all about ${chatbotData.heroData.name}.`,
                `Hi! 😊 Great to see you! Ask me anything about ${chatbotData.heroData.name}.`
            ];
            const greeting = greetings[Math.floor(Math.random() * greetings.length)];
            return greeting + "\n\nYou can ask me about:\n\n" +
                   "• Skills & Technologies 💻\n" +
                   "• Work Experience 💼\n" +
                   "• Projects 🚀\n" +
                   "• Education 🎓\n" +
                   "• Contact Information 📧\n\n" +
                   "What would you like to know?";
        }
    },

    skills: {
        keywords: ['skill', 'technology', 'tech stack', 'programming', 'languages', 'frameworks', 
                   'tools', 'what do you know', 'what can you do', 'expertise', 'technical skills',
                   'coding', 'development', 'software'],
        response: function() {
            if (chatbotData.skills.length === 0) {
                return "No skills information available at the moment.";
            }
            
            let response = `${chatbotData.heroData.name} is proficient in multiple technologies:\n\n`;
            
            for (const [category, skillNames] of Object.entries(chatbotData.skillsByCategory)) {
                response += `📌 ${category}:\n`;
                const categorySkills = chatbotData.skills.filter(s => s.category === category);
                categorySkills.forEach(skill => {
                    response += `   ${skill.icon || '•'} ${skill.name} - ${skill.proficiency}% proficiency\n`;
                });
                response += '\n';
            }
            
            return response + "Want to know more about a specific technology? Just ask!";
        }
    },
    
    skillCategory: {
        keywords: ['frontend', 'backend', 'database', 'devops', 'tools', 'design', 'ui', 'ux'],
        response: function(message) {
            const lowerMessage = message.toLowerCase();
            
            for (const [category, skillNames] of Object.entries(chatbotData.skillsByCategory)) {
                if (lowerMessage.includes(category.toLowerCase())) {
                    let response = `${category} Skills:\n\n`;
                    const categorySkills = chatbotData.skills.filter(s => s.category === category);
                    categorySkills.forEach(skill => {
                        response += `${skill.icon || '💻'} ${skill.name} - ${skill.proficiency}% proficiency\n`;
                    });
                    return response + `\n${chatbotData.heroData.name.split(' ')[0]} has strong expertise in ${category}!`;
                }
            }
            return null;
        }
    },
    
    experience: {
        keywords: ['experience', 'work', 'job', 'company', 'career', 'employment', 'worked', 
                   'working', 'professional', 'position', 'role'],
        response: function() {
            if (chatbotData.experiences.length === 0) {
                return "No work experience information available at the moment.";
            }
            
            let response = `${chatbotData.heroData.name} has impressive professional experience:\n\n`;
            
            chatbotData.experiences.forEach((exp, index) => {
                response += `🏢 ${exp.title} at ${exp.company}\n`;
                response += `   📅 ${exp.start_date} - ${exp.end_date}\n`;
                response += `   📍 ${exp.location}\n`;
                if (exp.technologies) {
                    response += `   💻 Tech: ${exp.technologies}\n`;
                }
                if (exp.is_current) {
                    response += `   ✨ Currently working here!\n`;
                }
                response += '\n';
            });
            
            return response;
        }
    },
    
    currentJob: {
        keywords: ['current job', 'currently working', 'present job', 'where work now', 
                   'current company', 'working now', 'current position'],
        response: function() {
            const currentExp = chatbotData.experiences.find(exp => exp.is_current);
            
            if (!currentExp) {
                return "Currently exploring new opportunities and open to exciting projects! 🚀";
            }
            
            return `${chatbotData.heroData.name.split(' ')[0]} is currently working as:\n\n` +
                   `💼 ${currentExp.title}\n` +
                   `🏢 ${currentExp.company}\n` +
                   `📍 ${currentExp.location}\n` +
                   `📅 Since ${currentExp.start_date}\n` +
                   `💻 Technologies: ${currentExp.technologies}\n\n` +
                   `${currentExp.description}`;
        }
    },
    
    specificSkill: {
        keywords: ['python', 'javascript', 'java', 'react', 'django', 'node', 'sql', 'git', 
                   'docker', 'html', 'css', 'mongodb', 'express', 'angular', 'vue', 'typescript'],
        response: function(message) {
            const lowerMessage = message.toLowerCase();
            
            for (const skill of chatbotData.skills) {
                if (lowerMessage.includes(skill.name.toLowerCase())) {
                    return `${skill.icon || '💻'} ${skill.name}\n\n` +
                           `Category: ${skill.category}\n` +
                           `Proficiency: ${skill.proficiency}%\n\n` +
                           `${chatbotData.heroData.name.split(' ')[0]} has ${skill.proficiency >= 80 ? 'excellent' : 'strong'} expertise in ${skill.name}! 🚀`;
                }
            }
            return null;
        }
    },
    
    projects: {
        keywords: ['project', 'built', 'created', 'developed', 'portfolio', 'work samples', 
                   'what have you built', 'showcase', 'demos'],
        response: "You can view all amazing projects in the portfolio section below! 🎨\n\n" +
                 "Each project showcases different skills and technologies with:\n" +
                 "• Live demos 🌐\n" +
                 "• Source code 💻\n" +
                 "• Detailed descriptions 📝\n\n" +
                 "Scroll down to explore the complete portfolio!"
    },
    
    education: {
        keywords: ['education', 'degree', 'study', 'college', 'university', 'qualification', 
                   'academic', 'graduated', 'studied', 'school'],
        response: function() {
            return `${chatbotData.heroData.name}'s educational background:\n\n` +
                   "🎓 Master of Computer Applications (MCA)\n" +
                   "   Specialized in Software Engineering\n" +
                   "   Advanced coursework in algorithms and system design\n\n" +
                   "🎓 Bachelor of Computer Science\n" +
                   "   Strong foundation in programming\n" +
                   "   Graduated with distinction";
        }
    },
    
    contact: {
        keywords: ['contact', 'email', 'phone', 'reach', 'hire', 'connect', 'message', 
                   'get in touch', 'call', 'mail', 'how to contact'],
        response: function() {
            return `You can reach ${chatbotData.heroData.name} through:\n\n` +
                   "📧 Email: arjunkmvat@gmail.com\n" +
                   "📱 Phone: +91 6282283144\n" +
                   "💼 LinkedIn: linkedin.com/in/arjun-k-m-12411022b\n" +
                   "💻 GitHub: github.com/arjun3031\n\n" +
                   "💡 Tip: Scroll down to the contact section to send a direct message!";
        }
    },
    
    about: {
        keywords: ['about', 'who are you', 'tell me about', 'introduction', 'bio', 
                   'describe yourself', 'who is', 'info about you'],
        response: function() {
            return `${chatbotData.heroData.name} - ${chatbotData.heroData.subtitle}\n\n` +
                   `${chatbotData.heroData.description}\n\n` +
                   `📊 Quick Stats:\n` +
                   `• ${chatbotData.experiences.length} Professional Experience(s)\n` +
                   `• ${chatbotData.skills.length} Technical Skills\n` +
                   `• Passionate about innovative solutions\n` +
                   `• Always learning and growing 🚀`;
        }
    },
    
    location: {
        keywords: ['location', 'where', 'based', 'live', 'from', 'home', 'city', 'place', 
                   'residence', 'hometown'],
        response: function() {
            const currentExp = chatbotData.experiences.find(exp => exp.is_current);
            const location = currentExp ? currentExp.location : "Kerala, India";
            return `📍 ${chatbotData.heroData.name} is based in ${location}\n\n` +
                   "A beautiful place with great tech opportunities! 🌴";
        }
    },
    
    technologies: {
        keywords: ['tech', 'technology stack', 'what technologies', 'programming languages', 
                   'tech used', 'stack'],
        response: function() {
            const allTechs = new Set();
            chatbotData.experiences.forEach(exp => {
                if (exp.technologies) {
                    exp.technologies.split(',').forEach(tech => {
                        allTechs.add(tech.trim());
                    });
                }
            });
            
            if (allTechs.size === 0) {
                return "Technologies information will be updated soon!";
            }
            
            return `Technologies used across various projects:\n\n` +
                   Array.from(allTechs).map(tech => `💻 ${tech}`).join('\n') +
                   `\n\n✨ Check the skills section for detailed proficiency levels!`;
        }
    },
    
    hire: {
        keywords: ['hire', 'available', 'freelance', 'contract', 'full time', 'part time', 
                   'looking for work', 'open to opportunities', 'recruiting'],
        response: function() {
            return `${chatbotData.heroData.name} is open to exciting opportunities! 🎯\n\n` +
                   "💼 Available for:\n" +
                   "• Full-time positions\n" +
                   "• Contract work\n" +
                   "• Freelance projects\n" +
                   "• Consulting\n\n" +
                   "🌟 Specializes in: Full Stack Development\n" +
                   "📧 Contact: arjunkmvat@gmail.com\n\n" +
                   "Let's build something amazing together! 🚀";
        }
    },
    
    thanks: {
        keywords: ['thank', 'thanks', 'appreciate', 'grateful', 'thx', 'ty'],
        response: function() {
            const responses = [
                `You're welcome! 😊 Is there anything else you'd like to know about ${chatbotData.heroData.name}?`,
                "Happy to help! 🎉 Feel free to ask more questions!",
                "My pleasure! 😄 What else would you like to know?"
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
    },
    
    goodbye: {
        keywords: ['bye', 'goodbye', 'see you', 'take care', 'later', 'cya', 'catch you later'],
        response: function() {
            const goodbyes = [
                "Goodbye! 👋 Feel free to come back anytime!",
                "Take care! 😊 Don't hesitate to reach out if you need anything!",
                "See you later! 🌟 Have a great day!"
            ];
            return goodbyes[Math.floor(Math.random() * goodbyes.length)];
        }
    },
    
    help: {
        keywords: ['help', 'what can you do', 'how to use', 'commands', 'options'],
        response: function() {
            return `I can help you learn about ${chatbotData.heroData.name}! 🤖\n\n` +
                   "Here's what you can ask:\n\n" +
                   "💻 Skills: 'What are your skills?', 'Tell me about Python'\n" +
                   "💼 Experience: 'Where do you work?', 'Tell me about your experience'\n" +
                   "🚀 Projects: 'Show me your projects'\n" +
                   "🎓 Education: 'What's your education?'\n" +
                   "📧 Contact: 'How can I reach you?'\n" +
                   "📍 Location: 'Where are you based?'\n\n" +
                   "Just ask naturally - I'll understand! 😊";
        }
    }
};

// AI Chatbot Elements
const chatButton = document.getElementById('chatButton');
const chatContainer = document.getElementById('chatContainer');
const chatCloseBtn = document.getElementById('chatCloseBtn');
const chatInput = document.getElementById('chatInput');
const chatSendBtn = document.getElementById('chatSendBtn');
const chatMessages = document.getElementById('chatMessages');
const typingIndicator = document.getElementById('typingIndicator');

// Scroll to bottom function
function scrollToBottom() {
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Toggle Chat - Open
if (chatButton) {
    chatButton.addEventListener('click', function() {
        chatContainer.classList.add('active');
        chatButton.classList.add('active');
        chatInput.focus();
        
        // Add welcome message if chat is empty
        if (chatMessages.children.length === 0) {
            addMessage(`Hello! 👋 I'm here to help you learn more about ${chatbotData.heroData.name}.\n\nYou can ask me about skills, experience, projects, education, or contact information!\n\nType 'help' to see all available commands.`, 'bot');
        }
        scrollToBottom();
    });
}

// Toggle Chat - Close
if (chatCloseBtn) {
    chatCloseBtn.addEventListener('click', function() {
        chatContainer.classList.remove('active');
        chatButton.classList.remove('active');
    });
}

// Send Message
function sendMessage() {
    const message = chatInput.value.trim();
    if (message === '') return;

    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';

    // Show typing indicator
    if (typingIndicator) {
        typingIndicator.classList.add('active');
    }
    scrollToBottom();

    // Generate bot response
    setTimeout(() => {
        const response = generateResponse(message);
        if (typingIndicator) {
            typingIndicator.classList.remove('active');
        }
        addMessage(response, 'bot');
        scrollToBottom();
    }, 800 + Math.random() * 700);
}

if (chatSendBtn) {
    chatSendBtn.addEventListener('click', sendMessage);
}

if (chatInput) {
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

// Add Message to Chat
function addMessage(text, sender) {
    if (!chatMessages) return;
    
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
    const lowerMessage = message.toLowerCase().trim();
    
    // Check knowledge base
    for (const [category, data] of Object.entries(knowledgeBase)) {
        if (data.keywords.some(keyword => lowerMessage.includes(keyword))) {
            const response = typeof data.response === 'function' ? data.response(message) : data.response;
            if (response) return response;
        }
    }

    // Default response with suggestions
    return `I'm not sure I understood that. 🤔\n\n` +
           `I can help you with:\n\n` +
           "• Skills & Technologies 💻\n" +
           "• Work Experience 💼\n" +
           "• Projects 🚀\n" +
           "• Education 🎓\n" +
           "• Contact Info 📧\n" +
           "• Location 📍\n\n" +
           "Try asking something like:\n" +
           "- 'What are your skills?'\n" +
           "- 'Where do you work?'\n" +
           "- 'How can I contact you?'\n\n" +
           "Type 'help' for more options!";
}

// Password toggle
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');
    
    if (passwordInput && toggleIcon) {
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
}

// Change Password Modal
function openModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) {
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = 'auto';
        const changePasswordForm = document.getElementById('changePasswordForm');
        if (changePasswordForm) {
            changePasswordForm.reset();
        }
    }
}

function closeModalOnOverlay(event) {
    if (event.target === event.currentTarget) {
        closeModal();
    }
}

function togglePasswordField(fieldId) {
    const input = document.getElementById(fieldId);
    if (input) {
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
    }
}