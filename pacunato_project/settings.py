"""
Django settings for pacunato_project project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================
# SEGURIDAD
# ============================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-(_uhp$g(3ab3##__kifw^o2fyn2%w^gi&phid4=n+iq+5%vht1'
)

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1'
).split(',')


# ============================================
# APLICACIONES
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'website',
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

ROOT_URLCONF = 'pacunato_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'website', 'templates')],
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

WSGI_APPLICATION = 'pacunato_project.wsgi.application'


# ============================================
# BASE DE DATOS
# ============================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================
# INTERNACIONALIZACIÓN
# ============================================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Panama'
USE_I18N = True
USE_TZ = True


# ============================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ============================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary para media en producción
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }
else:
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }


# ============================================
# CONFIGURACIÓN DE EMAIL (Hostinger SMTP)
# ============================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'info@pacunato.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'Pacunato S.A. <info@pacunato.com>'
SERVER_EMAIL = 'info@pacunato.com'
CONTACT_EMAIL = 'info@pacunato.com'


# ============================================
# WEBHOOKS DE AUTOMATIZACIÓN
# ============================================

# Make.com (legacy - siendo migrado a n8n)
MAKE_WEBHOOK_ASESORIA = os.environ.get(
    'MAKE_WEBHOOK_ASESORIA',
    'https://hook.eu2.make.com/TU_WEBHOOK_ID_ASESORIA'
)
MAKE_WEBHOOK_COTIZACION = os.environ.get(
    'MAKE_WEBHOOK_COTIZACION',
    'https://hook.eu2.make.com/TU_WEBHOOK_ID_COTIZACION'
)

# n8n (nuevo)
N8N_WEBHOOK_BASE_URL = os.environ.get(
    'N8N_WEBHOOK_BASE_URL',
    'https://eduarodriguez.app.n8n.cloud/webhook/'
)
