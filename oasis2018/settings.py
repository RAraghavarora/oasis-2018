import os
import datetime
from oasis2018.settings_config import keyconfig

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

DEBUG = keyconfig.DEBUG

SECRET_KEY = keyconfig.SECRET_KEY

SERVER = keyconfig.SERVER



# Application definition

INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'corsheaders',
    'rest_framework',
    'rest_framework_jwt',

    'events',
    'regsoft',
    'pcradmin',
    'analytics',
    'registrations',
    'preregistration',
    'shop.apps.ShopConfig',
    'ems.apps.EmsConfig',
    'wordwars',
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
    #'wordwars.middleware.WordWarsMiddleware',
    'pcradmin.middleware.PCrAdminMiddleware',
]


if keyconfig.SERVER:
    MIDDLEWARE.append('oasis2018.middlewares.AppException')


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

#MC Ab change mat krna isko
if keyconfig.SERVER:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': keyconfig.DATABASE_NAME,
            'USER': keyconfig.DATABASE_USER,
            'PASSWORD': keyconfig.DATABASE_PASSWORD,
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
else:
    print("Using SQLite3 locally.")
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
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
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

GOOGLE_RECAPTCHA_SECRET_KEY = keyconfig.google_recaptcha_secret_key
GOOGLE_RECAPTCHA_SITE_KEY = keyconfig.google_recaptcha_site_key


# APPEND_SLASH = False

LOGIN_URL = '/2018/registrations/login/'
# LOGOUT_REDIRECT_URL = '/registrations/login/'

CORS_ORIGIN_ALLOW_ALL = True

JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=365)
}


#Logging
'''
BASE_DIR is being used in oasis2018.loggers,
so this import can only occur after it has been declared.

Use logging_tree module to visualize logging structure.
'''
import raven

RAVEN_CONFIG = {
    'dsn': 'https://0830bb2a73324f2f8d8082acf42fb52c:1b167f754ba54602825fe60a5e87bffa@sentry.io/1276415',
}
