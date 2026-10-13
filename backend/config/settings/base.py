import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'apps.parts',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


WSGI_APPLICATION = 'config.wsgi.application'


def mssql_database(name):
    """Connection settings for one database on the shared SQL Server."""
    return {
        'ENGINE': 'mssql',
        'NAME': name,
        'HOST': os.environ.get('MSSQL_HOST', 'localhost'),
        'PORT': os.environ.get('MSSQL_PORT', '1433'),
        'USER': os.environ.get('MSSQL_USER', ''),
        'PASSWORD': os.environ.get('MSSQL_PASSWORD', ''),
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': os.environ.get('MSSQL_EXTRA_PARAMS', ''),
        },
    }


# `default` is the platform database, owned by Django migrations. `parts` is
# the existing parts database; its structure is never changed by the platform.
DATABASES = {
    'default': mssql_database(os.environ.get('PLATFORM_DB_NAME', 'ee_platform')),
    'parts': mssql_database(os.environ.get('PARTS_DB_NAME', 'ee_parts')),
}

DATABASE_ROUTERS = ['config.db_routers.PartsRouter']


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


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'EE Platform API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
