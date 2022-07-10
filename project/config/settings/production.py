import os

from config.settings.base import *

from dotenv import load_dotenv

from pathlib import Path

from config.settings.base import *


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # where manage.py is

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/media/"
