
from pathlib import Path
import os
from django.contrib import messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lycz&q+-#*01*()h68f!=3-p5a$qc8*jn$w+!5%0!!8*3i8)=8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',  # Django Axes for login attempt tracking
    'app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',  # Must be after AuthenticationMiddleware
    'app.middlewares.NoCacheMiddleware',
    'app.middlewares.SessionSecurityMiddleware',  # Custom security middleware
]

ROOT_URLCONF = 'myportfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myportfolio.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portfolio_db',
        'USER': 'root',
        'PASSWORD': 'arjun3031',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}


AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Session cookies security
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
SESSION_COOKIE_AGE = 3600  # 1 hour (in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Clear session on browser close
SESSION_SAVE_EVERY_REQUEST = True  # Reset timeout on each request

SESSION_COOKIE_SECURE = False

# Session engine
SESSION_ENGINE = 'django.contrib.sessions.backends.db'



CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = True  # Store CSRF token in session instead of cookie
CSRF_FAILURE_VIEW = 'app.views.csrf_failure'

CSRF_COOKIE_SECURE = False 

# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True

# For development, set these to False. For production with HTTPS, set to True
SECURE_SSL_REDIRECT = False  # Redirect HTTP to HTTPS
SECURE_HSTS_SECONDS = 0  # HTTP Strict Transport Security (set to 31536000 in production)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False


# Lock account after 5 failed attempts
AXES_FAILURE_LIMIT = 5

# Lock duration: 1 hour
AXES_COOLOFF_TIME = 1  # In hours

# Lock out on failure
AXES_LOCK_OUT_AT_FAILURE = True

# Reset failed attempts on successful login
AXES_RESET_ON_SUCCESS = True

# Lock by combination of username and IP
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True

# Username form field
AXES_USERNAME_FORM_FIELD = 'username'

# Enable axes in admin
AXES_ENABLE_ADMIN = True

# Verbose logging
AXES_VERBOSE = True

# Custom lockout template
AXES_LOCKOUT_TEMPLATE = 'account_locked.html'

# Custom lockout URL
AXES_LOCKOUT_URL = '/locked/'

# Only track user failures (not anonymous)
AXES_ONLY_USER_FAILURES = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'formatter': 'verbose',
        },
        'axes_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'login_attempts.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'axes.watch_login': {
            'handlers': ['axes_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'app': {
            'handlers': ['security_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# message

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Cache middleware settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 0  # Disable caching
CACHE_MIDDLEWARE_KEY_PREFIX = ''


# ============================================
# SECURITY NOTES FOR PRODUCTION
# ============================================

"""
BEFORE DEPLOYING TO PRODUCTION, CHANGE THESE SETTINGS:

1. Set DEBUG = False
2. Update ALLOWED_HOSTS with your domain
3. Generate new SECRET_KEY and store in environment variable
4. Set SESSION_COOKIE_SECURE = True (requires HTTPS)
5. Set CSRF_COOKIE_SECURE = True (requires HTTPS)
6. Set SECURE_SSL_REDIRECT = True (requires HTTPS)
7. Set SECURE_HSTS_SECONDS = 31536000
8. Set SECURE_HSTS_INCLUDE_SUBDOMAINS = True
9. Set SECURE_HSTS_PRELOAD = True
10. Remove database password from settings (use environment variables)
11. Setup proper SSL certificate (Let's Encrypt)
12. Enable firewall and restrict database access
13. Regular security updates: pip install --upgrade django django-axes

Example production settings:
    DEBUG = False
    ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
"""