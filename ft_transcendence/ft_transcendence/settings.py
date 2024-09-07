"""
Django settings for ft_transcendence project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

DOMAIN_NAME='deciding-delicate-raptor.ngrok-free.app'

from pathlib import Path
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import hvac
with open('/vault/token-volume/rootToken', 'r') as file:
    vault_token = file.read().strip()
client = hvac.Client(url='http://vault:8200', token=vault_token)
secret = client.secrets.kv.v2.read_secret_version(path='postgresql/db_credentials')['data']['data']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': secret['db_name'],
        'USER': secret['db_user'],
        'PASSWORD': secret['db_password'],
        'HOST': secret['db_host'],
        'PORT': secret['db_port'],
    }
}

PRIVATE_KEY=secret['private_key']
INFURA_URL=secret['infura_url']
CONTRACT_ADDRESS=secret['contract_address']
DEPLOYER_ACCOUNT=secret['deployer_account']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-$0x^=vch)m=$7%i7abn6=nuhwe8w!0nl#$ays34#q3f+90-dm='
SECRET_KEY = secret['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = secret['DEBUG']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



ALLOWED_HOSTS = ['localhost', '127.0.0.1', secret['domain_name'], secret['localip']]

localip = "https://" +  secret['localip'] 
domain_name = "https://" + secret['domain_name']

CSRF_TRUSTED_ORIGINS = [
    'https://localhost',
    'https://127.0.0.1',
    domain_name,
    localip,
    # 'https://yourdomain.com',
]

# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_HOST_USER = 'da5b061fad8477'
# EMAIL_HOST_PASSWORD = 'f9ee2539a9b31b'
# EMAIL_PORT = '2525'
# DEFAULT_FROM_EMAIL="PingPong_QTOR@gmail.com"
# EMAIL_USE_TLS=True

EMAIL_BACKEND=secret['EMAIL_BACKEND']
EMAIL_HOST=secret['EMAIL_HOST']
EMAIL_HOST_USER=secret['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD=secret['EMAIL_HOST_PASSWORD']
EMAIL_PORT=secret['EMAIL_PORT']
# EMAIL_USE_TLS=secret['EMAIL_USE_TLS']
# EMAIL_USE_SSL=secret['EMAIL_USE_SSL']
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False


# Application definition


INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
    'users',
    'game',
    'chat',
    'crypto',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

ASGI_APPLICATION = 'ft_transcendence.asgi.application'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'game.middleware.CleanupMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'users.middleware.CookieToAuthorizationMiddleware',
]

ROOT_URLCONF = 'ft_transcendence.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'ft_transcendence.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = "users.User"



CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Use Redis server URL here
    }
}

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
    'ALGORITHM': 'HS256',
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}

INITIALIZED_1 = False



INTERNAL_IPS = [
    '127.0.0.1',
]