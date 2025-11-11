from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_str.split(',') if h.strip()]
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']
else:
    if '127.0.0.1' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('127.0.0.1')
    if 'localhost' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('localhost')
    if 'testserver' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('testserver')
    if 'agentdocai-production.up.railway.app' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('agentdocai-production.up.railway.app')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
if 'https://agentdocai-production.up.railway.app' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append('https://agentdocai-production.up.railway.app')

APPEND_SLASH = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mcp_manager'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mcp_integration.urls'

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

WSGI_APPLICATION = 'mcp_integration.wsgi.application'

import dj_database_url
import psycopg2

DATABASES = {}
use_postgres = False

if 'DATABASE_URL' in os.environ:
    try:
        db_config = dj_database_url.config(
            conn_max_age=500,
            conn_health_checks=True,
        )
        if db_config and db_config.get('ENGINE') == 'django.db.backends.postgresql':
            try:
                conn_params = {
                    'host': db_config.get('HOST'),
                    'port': db_config.get('PORT'),
                    'user': db_config.get('USER'),
                    'password': db_config.get('PASSWORD'),
                    'dbname': db_config.get('NAME'),
                    'connect_timeout': 5
                }
                test_conn = psycopg2.connect(**{k: v for k, v in conn_params.items() if v is not None})
                test_conn.close()
                use_postgres = True
                DATABASES['default'] = db_config
                DATABASES['default']['OPTIONS'] = {
                    'connect_timeout': 10,
                    'options': '-c statement_timeout=30000'
                }
            except (psycopg2.OperationalError, psycopg2.Error, Exception):
                use_postgres = False
    except Exception:
        use_postgres = False

if not use_postgres:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN', '')

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True