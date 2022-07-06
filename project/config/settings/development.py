import os

from config.settings.base import *

from dotenv import load_dotenv

from pathlib import Path


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # where manage.py is

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
