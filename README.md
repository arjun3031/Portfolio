# Arjun K M - Professional Portfolio Website

A modern, feature-rich portfolio website built with Django, Python, and contemporary web technologies. Showcasing professional skills, experience, projects, and education with a secure admin panel and interactive chatbot.

**Live Demo:** [https://arjunkm3031.pythonanywhere.com/](https://arjunkm3031.pythonanywhere.com/)

---

## Screenshots

### Homepage
![Portfolio Homepage](assets/homepage.png)
*Professional portfolio homepage with introduction, skills overview, and call-to-action buttons*

### Admin Dashboard
![Admin Dashboard](assets/admin-dashboard.png)
*Admin panel dashboard showing inquiry statistics, skills overview, and management options*

---

## Features

###  User-Facing Features
- **Dynamic Home Page** - Professional portfolio introduction with engaging content about career highlights
- **Skills Section** - Comprehensive display of technical expertise with proficiency levels
- **Experience Timeline** - Professional work history and career progression
- **Projects Showcase** - Detailed portfolio of completed projects
- **Education Details** - Academic qualifications and certifications
- **Contact Section** - Direct contact information and inquiry form
- **AI-Powered Chatbot** - Interactive assistant for visitors to:
  - Query skills and expertise
  - Learn about projects and experience
  - Access education details
  - Retrieve contact information and location
  - Engage with fun facts about the developer
- **Responsive Design** - Optimized for desktop, tablet, and mobile viewing
- **Inquiry System** - Allow visitors to send messages for professional inquiries

###  Admin Panel Features
- **Secure Authentication** - Account lockout mechanism (1-hour lockout after invalid credentials)
- **Dashboard Overview** - View inquiry messages with unread message counts
- **Content Management**
  - Add, edit, update, and delete portfolio content
  - Manage images and media assets
  - Update professional information
- **Skills Management** - Add, edit, update, and delete skills by category
- **Experience Management** - Manage professional work history
- **Project Management** - Create and maintain project portfolio
- **Education Management** - Add educational qualifications and certifications
- **Security Features**
  - Password reset functionality
  - Forgot password recovery
  - Session management with auto-logout
- **Metadata Tracking** - View publication dates and author information

### Security Features
- VAPT (Vulnerability Assessment & Penetration Testing) compliant
- Input validation and sanitization
- Account lockout protection against brute force attacks
- Session management with timeout handling
- Secure password reset mechanism
- CSRF protection
- SQL injection prevention

---

## Technology Stack

| Category | Technologies |
|----------|---------------|
| **Backend** | Django, Python |
| **Frontend** | HTML5, CSS3, Bootstrap, JavaScript |
| **Database** | MySQL (MySQL Workbench) |
| **IDE** | Visual Studio Code |
| **AI/Chatbot** | Conversational AI Integration |
| **Hosting** | PythonAnywhere |
| **Security** | VAPT-Compliant Architecture |# 🚀 Arjun K M - Professional Portfolio Website

---

## Project Structure

```
portfolio-website/
├── manage.py
├── portfolio/                    # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── apps/
│   ├── home/                    # Home page app
│   ├── skills/                  # Skills management
│   ├── experience/              # Experience management
│   ├── projects/                # Projects management
│   ├── education/               # Education management
│   ├── contact/                 # Contact & inquiry system
│   ├── chatbot/                 # AI chatbot integration
│   └── admin_dashboard/         # Admin panel
├── static/                      # CSS, JS, images
├── templates/                   # HTML templates
└── requirements.txt
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MySQL Server
- Virtual Environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolio-website
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Update `settings.py` with MySQL credentials
   - Run migrations:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Portfolio: `http://localhost:8000/`
   - Admin Panel: `http://localhost:8000/admin/`

---

## User Interface

### Public Portfolio Pages
- **Home** - Professional introduction and overview
- **About** - Career summary and professional highlights
- **Skills** - Technical expertise with proficiency indicators
- **Experience** - Work history and professional journey
- **Projects** - Showcase of completed projects
- **Education** - Academic credentials and certifications
- **Contact** - Direct contact methods and inquiry form
- **Chatbot** - Interactive AI assistant available throughout the site

### Admin Dashboard
- **Dashboard Overview** - Inquiry statistics and unread message counter
- **Manage Content** - Update portfolio content and media
- **Manage Skills** - CRUD operations for skills database
- **Manage Experience** - Add and edit work experience
- **Manage Projects** - Maintain project portfolio
- **Manage Education** - Update educational information
- **Account Security** - Password management and logout functionality

---

## Security Implementation

- **Authentication** - Secure login with credential validation
- **Authorization** - Role-based access control (Admin only)
- **Account Lockout** - 1-hour lockout after 3 failed login attempts
- **Session Management** - Automatic session expiration and cleanup
- **Input Validation** - All user inputs validated and sanitized
- **SQL Injection Prevention** - Parameterized queries throughout
- **CSRF Protection** - Django CSRF middleware enabled
- **Password Security** - Hashed password storage with salt

---

## 🤖 Chatbot Capabilities

The interactive chatbot assists visitors by providing information about:
- Professional skills and expertise
- Work experience and career details
- Completed projects and accomplishments
- Educational background and certifications
- Contact information and location
- Fun facts and personal interests

---

## Key Statistics

- **Skills:** 5+ technical proficiencies
- **Experiences:** 2+ professional positions
- **Projects:** Showcase portfolio
- **Education:** Multiple certifications and degrees
- **Inquiries:** Real-time message tracking
- **Response Rate:** Admin dashboard for inquiry management

---

## Admin Workflow

1. **Login** - Access admin panel with secure credentials
2. **Dashboard** - Monitor incoming inquiries and statistics
3. **Content Management** - Update portfolio information
4. **User Communications** - Review and respond to visitor inquiries
5. **Data Maintenance** - Add/edit/delete skills, experience, projects, education
6. **Security** - Manage passwords and sessions
7. **Logout** - Secure session termination

---

## Responsive Design

The portfolio is fully responsive and optimized for:
- 🖥️ Desktop (1920px and above)
- 💻 Laptop (1024px - 1920px)
- 📱 Tablet (768px - 1024px)
- 📲 Mobile (320px - 768px)

---

## Future Enhancements

- **Theme Customization** - Dark/Light mode toggle and color themes
- **Advanced AI Integration** - GPT-powered chatbot for enhanced conversations
- **Modern Security** - OAuth2 integration and two-factor authentication (2FA)
- **Cloud Storage** - Migrate from MySQL to cloud-based solutions
- **Performance** - CDN integration and caching optimization
- **Analytics** - Visitor tracking and behavior analytics
- **Blog Section** - Article publishing and content management
- **Portfolio Recommendations** - AI-driven content suggestions

---

## Deployment

The website is currently deployed on **PythonAnywhere** and is accessible at:
```
https://arjunkm3031.pythonanywhere.com/
```

### Deployment Steps
1. Ensure all requirements are listed in `requirements.txt`
2. Configure database on hosting platform
3. Set environment variables for security
4. Run migrations on production database
5. Collect static files
6. Configure web server (WSGI)
7. Enable HTTPS/SSL certificate

---

## Usage Guide

### For Visitors
1. Browse portfolio sections to learn about skills and experience
2. Interact with the chatbot for quick information
3. Submit inquiries through the contact form
4. Download resume for offline reference

### For Admin
1. Log in with credentials at `/admin/`
2. View incoming inquiries in dashboard
3. Manage portfolio content through respective menus
4. Update personal information as needed
5. Monitor security and session activity
6. Log out after completing tasks

---

## Contributing

Contributions, suggestions, and improvements are welcome! Please feel free to:
- Report issues or bugs
- Suggest new features
- Improve documentation
- Submit pull requests

---

## Contact & Inquiry

- **Website:** [https://arjunkm3031.pythonanywhere.com/](https://arjunkm3031.pythonanywhere.com/)
- **Contact Form:** Available on the website
- **Chatbot:** Available 24/7 on the portfolio

---

## License

This project is created for professional portfolio purposes. All rights reserved.

---

## About

This portfolio website showcases professional expertise in Software Engineering with a focus on building exceptional digital experiences using modern technologies and best practices.

**Developed with using Django & Python**

---

## Performance & SEO

- Fast loading times with optimized assets
- Mobile-first responsive design
- SEO-friendly structure
- Accessibility compliance (WCAG standards)
- Cross-browser compatibility

---

**Last Updated:** November 2025  
**Status:** ✅ Active and Maintained
