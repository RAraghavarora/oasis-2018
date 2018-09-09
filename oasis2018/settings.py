try:
    from oasis2018.keyconfig import *    # Production
    DEBUG = Debug              # Created debug variable in the keyconfig file, which can be changed whenever required
except:
    DEBUG = True

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'preregistration',
    'events',
    'registrations',
    'analytics',
    'shop.apps.ShopConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

try:
    if SERVER:
        MIDDLEWARE.append('oasis2018.middlewares.AppException')
except:
    pass

ROOT_URLCONF = 'oasis2018.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'oasis2018.wsgi.application'

try:
    from oasis2018.keyconfig import *
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
except Exception as error_message:
    print("DATABASE SETTINGS ERROR: {}".format(error_message))
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

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
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/backend_static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/backend_media/'

GOOGLE_RECAPTCHA_SECRET_KEY = google_recaptcha_secret_key

APPEND_SLASH = False

# LOGIN_URL = '/2018/register/login/'


CORS_ORIGIN_ALLOW_ALL = True

#settings.py update


#Logging
'''
BASE_DIR is being used in oasis2018.loggers, 
so this import can only occur after it has been declared.

Use logging_tree module to visualize logging structure.
'''

from oasis2018 import loggers
import raven

RAVEN_CONFIG = {
    'dsn': 'https://0830bb2a73324f2f8d8082acf42fb52c:1b167f754ba54602825fe60a5e87bffa@sentry.io/1276415',
}
#from raven.contrib.django.raven_compat.models import client
#client.captureException()