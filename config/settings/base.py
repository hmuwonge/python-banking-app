

from pathlib import Path

import cloudinary
from django.conf.global_settings import STATIC_ROOT, LOGGING, AUTH_USER_MODEL
from dotenv import load_dotenv
from os import getenv, path
from loguru import logger
from datetime import timedelta, date

# from config.settings import INSTALLED_APPS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = BASE_DIR/"core_apps"

local_env_file =path.join(BASE_DIR, ".envs",".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)
# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/
#
# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-4*tt4imy%0a1b#@4yawso411c&elh1&dlj*&w3y072_c_60kgi'
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
#
# ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_countries',
    'phonenumber_field',
    'drf_spectacular',
    'djoser',
    'cloudinary',
    'django_filters',
    'djcelery_email',
    'django_celery_beat',
]

LOCAL_APPS=["core_apps.user_auth","core_apps.common","core_apps.user_profile"]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "core_apps.user_auth.middleware.CustomHeaderMiddleware"
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR/"templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv("POSTGRES_DB"),
        'USER': getenv("POSTGRES_USER"),
        'PASSWORD': getenv("POSTGRES_PASSWORD"),
        'HOST': getenv("POSTGRES_HOST"),
        'PORT': getenv("POSTGRES_PORT"),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
SITE_ID =1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR/"staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "user_auth.User"
DEFAULT_BIRTH_DATE = date(1900,1,1)
DEFAULT_DATE = date(2000,1,1)
DEFAULT_EXPIRY_DATE = date(2026,1,1)
DEFAULT_COUNTRY ="UG"
DEFAULT_PHONE_NUMBER= "+256704348792"
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "NextGen Bank API",
    "DESCRIPTION": "An API built for a banking system",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE":{
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
}

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND_MAX_RETIRES =10
CELERY_TASK_SEND_SENT_EVENT =True
CELERY_RESULT_EXTENDED =True
CELERY_RESULT_BACKEND_ALWAYS_RETRY =True
CELERY_TASK_TIME_LIMIT =5*60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_BEAT_SCHEDULER ="django_celery_beat.schedulers.DatabaseScheduler"
CELERY_WORKER_SEND_TASK_EVENTS = True

CLOUDINARY_CLOUD_NAME = getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

LOGGING_CONFIG = None
LOGURU_LOGGING = {
    "handlers":[
        {
            "level": "DEBUG",
            "sink": BASE_DIR/"logs/debug.log",
            "filter": lambda  record: record["level"].no <= logger.level("WARNING").no,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line}- {message}",
            "rotation": "10MB",
            "retention":"30 days",
            "compression": "zip",
        },
        {
            "level": "DEBUG",
            "sink": BASE_DIR/"logs/error.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line}- {message}",
            "rotation": "10MB",
            "retention":"30 days",
            "compression": "zip",
            "backtrace": True,
            "diagnose": True
        }
    ]
}
logger.configure(**LOGURU_LOGGING)

LOGGING = {
"version": 1,
"disable_existing_loggers": False,
"handlers": {"loguru": {"class": "interceptor. InterceptHandler"}},
"root": {"handlers": ["loguru"], "level": "DEBUG"}
}