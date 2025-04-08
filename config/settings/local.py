from os import getenv, path

from django.conf.global_settings import EMAIL_BACKEND, EMAIL_HOST
from dotenv import load_dotenv
from .base import * # noqa
from .base import BASE_DIR
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")

SITE_NAME = getenv("SITE_NAME")

ALLOWED_HOSTS = ["localhost","127.0.0.1","0.0.0.0"]
ADMIN_URL = getenv("ADMIN_URL")

EMAIL_BACKEND ="djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_port")
DEFAUlT_FROM_EMAIL = getenv("DEFAUlT_FROM_EMAIL")
DOMAIN = getenv("DOMAIN")
MAX_UPLOAD_SIZE=1 * 1024* 1024