from .base import *

DEBUG = False


SECRET_KEY = 'django-insecure-testing-only'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
