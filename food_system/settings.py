"""
Django settings for food_system project.
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Django's MySQL backend expects a MySQLdb-compatible driver.
# PyMySQL is installed as MySQLdb so django.db.backends.mysql works.
try:
    import pymysql  # type: ignore
    pymysql.install_as_MySQLdb()
except Exception:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
_DEFAULT_INSECURE_SECRET_KEY = (
    'django-insecure-i3^r_g7c*8xg@=dkxbr+^yszd)pk$^tqb6gyy805!r_n%6o*xf'
)
SECRET_KEY = config('SECRET_KEY', default=_DEFAULT_INSECURE_SECRET_KEY)

DEBUG = config('DEBUG', default=True, cast=bool)
FORCE_HTTPS = config('FORCE_HTTPS', default=not DEBUG, cast=bool)


def _csv_env(name: str, default: str = '') -> list:
    value = config(name, default=default)
    return [part.strip() for part in value.split(',') if part.strip()]


ALLOWED_HOSTS = _csv_env('ALLOWED_HOSTS', 'localhost,127.0.0.1,.onrender.com')
CSRF_TRUSTED_ORIGINS = _csv_env('CSRF_TRUSTED_ORIGINS', '')

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'customers',
    'chef',
    'orders',
    'management',
]

AUTH_USER_MODEL = 'customers.CustomUser'
LOGIN_URL = 'customers:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'food_system.middleware.NoCacheMiddleware',
]

ROOT_URLCONF = 'food_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'food_system.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASE_URL = config('DATABASE_URL', default='')
DB_ENGINE   = config('DB_ENGINE',   default='django.db.backends.sqlite3')
DB_NAME     = config('DB_NAME',     default=str(BASE_DIR / 'db.sqlite3'))
DB_USER     = config('DB_USER',     default='')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST     = config('DB_HOST',     default='localhost')
DB_PORT     = config('DB_PORT',     default='3306')

if DATABASE_URL:
    _db = dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
            ssl_require=False,  # Don't use sslmode — not MySQL compatible
        )
    # TiDB Cloud Serverless requires SSL — inject OPTIONS for PyMySQL
    _db.setdefault('OPTIONS', {})
    _db['OPTIONS']['ssl'] = {'ssl_verify_cert': False}
    # Remove sslmode key if dj_database_url added it (PostgreSQL-only param)
    _db.pop('sslmode', None)
    _db.get('OPTIONS', {}).pop('sslmode', None)
    DATABASES = {'default': _db}
elif DB_ENGINE == 'django.db.backends.mysql':
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DB_NAME,
        }
    }

# ---------------------------------------------------------------------------
# Password validation
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ---------------------------------------------------------------------------
# Production security hardening  (only active when DEBUG=False)
# ---------------------------------------------------------------------------
if not DEBUG:
    if SECRET_KEY == _DEFAULT_INSECURE_SECRET_KEY:
        raise RuntimeError(
            'SECRET_KEY must be set to a strong value when DEBUG=False. '
            'Set the SECRET_KEY environment variable on your host (e.g. Render).'
        )

    SECURE_SSL_REDIRECT = FORCE_HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=3600, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=False, cast=bool)
    X_FRAME_OPTIONS = 'DENY'

# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Must be False so JS can read CSRF token in forms


# ---------------------------------------------------------------------------
# Logging — console always; file only when the logs/ dir exists (local dev)
# ---------------------------------------------------------------------------
_LOG_DIR = os.path.join(BASE_DIR, 'logs')
_USE_FILE_LOG = os.path.isdir(_LOG_DIR)

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
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        **({
            'file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': os.path.join(_LOG_DIR, 'django.log'),
                'formatter': 'verbose',
            }
        } if _USE_FILE_LOG else {}),
    },
    'root': {
        'handlers': ['console', 'file'] if _USE_FILE_LOG else ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'] if _USE_FILE_LOG else ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
