from .base import *

DEBUG = False


SECRET_KEY = 'django-insecure-testing-only'


# Tests run on in-memory SQLite so they need neither Docker nor SQL Server.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'parts': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
