import os
from pathlib import Path

# Обновляем BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'replacer_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sql_replacer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sql_replacer.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Production settings
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings for production
if os.environ.get('DEBUG', 'True').lower() in ('false', '0', 'f'):
    DEBUG = False

    # Security settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # HTTPS settings (uncomment when SSL is configured)
    # SECURE_SSL_REDIRECT = True
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Static files
    STATIC_ROOT = BASE_DIR / 'static'
    STATIC_URL = '/static/'

    # Allowed hosts
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    # Add your domain here
    yc_host = os.environ.get('YC_HOST', '')
    if yc_host:
        ALLOWED_HOSTS.append(yc_host)

    # Parse ALLOWED_HOSTS from environment
    env_hosts = os.environ.get('ALLOWED_HOSTS', '')
    if env_hosts:
        ALLOWED_HOSTS.extend([h.strip() for h in env_hosts.split(',')])

else:
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    STATIC_URL = 'static/'