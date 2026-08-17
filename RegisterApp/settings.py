"""
Django settings for RegisterApp project.
"""

from pathlib import Path
import os
import dj_database_url
from environ import Env
from numpy import True_

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Load .env ─────────────────────────────────────────────────────────────────
env = Env()
Env.read_env(os.path.join(BASE_DIR, '.env'))

# ── Environment ───────────────────────────────────────────────────────────────
ENVIRONMENT = env('ENVIRONMENT', default='development')
IS_PRODUCTION = ENVIRONMENT == 'production'
if ENVIRONMENT == 'development':
    DEBUG=True
else:
    DEBUG=False

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = env('SECRET_KEY')
DEBUG = not IS_PRODUCTION
ALLOWED_HOSTS = ['.vercel.app', 'now.sh', '127.0.0.1', 'localhost'] if IS_PRODUCTION else ['*']

# ── CSRF trusted origins (required for Vercel) ────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
]

# ── Installed apps ────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project
    'core',

    # third-party
    'import_export',
    'whitenoise.runserver_nostatic',   # must come after staticfiles
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # serve static files on Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.RestrictDjangoAdminMiddleware',
]

ROOT_URLCONF = 'RegisterApp.urls'

# ── Templates ─────────────────────────────────────────────────────────────────
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

WSGI_APPLICATION = 'RegisterApp.wsgi.application'

# ── Database ──────────────────────────────────────────────────────────────────
# Development: SQLite
# Production:  Neon PostgreSQL via DATABASE_URL in .env
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

NEON_DATABASE_LOCALLY = False #when i want to use hosted database locally

if ENVIRONMENT == 'production' or NEON_DATABASE_LOCALLY == True:
    DATABASE_URL = env('DATABASE_URL', default='')
    if DATABASE_URL:
        DATABASES['default'] = dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,          # keep connections alive 10 min
            conn_health_checks=True,   # auto-reconnect if connection drops
            ssl_require=True,          # Neon requires SSL
        )

# ── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# WhiteNoise: compress + cache static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media files ───────────────────────────────────────────────────────────────
# Note: Vercel is read-only — media uploads won't persist.
# Use Cloudinary or an S3 bucket for user-uploaded files in production.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── Misc ──────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL          = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
