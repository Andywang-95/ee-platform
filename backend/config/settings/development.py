import os

from .base import *

DEBUG = True


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-only')


# `backend` is the service name the frontend dev server proxies to in compose.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']
