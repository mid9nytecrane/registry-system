"""
Django settings for RegisterApp project.
"""

from pathlib import Path
import os
from environ import Env
import dj_database_url





# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent


env = Env()
#Env.read_env()  
Env.read_env(os.path.join(BASE_DIR, '.env'))

ENVIRONMENT = env('ENVIRONMENT', default='production')

# ── Security ────────────────────────────────────────────────────────────────
# Reads SECRET_KEY from .env; falls back to the insecure dev key if missing
# so the project still starts without a .env file in development.

SECRET_KEY = env('SECRET_KEY')


if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False 



if ENVIRONMENT == 'development':
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', 'now.sh']


# ── Installed apps ───────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',

    # project apps
    'core',

    # third-party
    'import_export',
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
# Default: SQLite for development.
# For production set DATABASE_URL in .env and uncomment the dj-database-url block.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

POSTGRES_LOCALLY = False # True if want to access postgres data while running locally
if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
    DATABASES['default'] = dj_database_url.parse(env("DATABASE_URL"))


# Production database (uncomment when deploying):
# import dj_database_url
# DATABASE_URL = config('DATABASE_URL', default='')
# if DATABASE_URL:
#     DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)

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

# ── Static & Media files ──────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── Misc ──────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'
