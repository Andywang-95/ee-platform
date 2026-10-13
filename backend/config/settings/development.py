import os

from .base import *

DEBUG = True


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-only')


# `backend` is the service name the frontend dev server proxies to in compose.
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']


# Login arrives in M3. Until then the development environment serves the API
# without it; testing and production keep the IsAuthenticated default.
REST_FRAMEWORK = {
    **REST_FRAMEWORK,
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}
