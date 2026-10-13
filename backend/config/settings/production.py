import os

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = False


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    raise ImproperlyConfigured('DJANGO_SECRET_KEY must be set when using production settings.')


ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',') if host.strip()
]


# Placeholder until the dual-database setup lands in M1; production will
# connect to SQL Server using connection settings from the environment.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
