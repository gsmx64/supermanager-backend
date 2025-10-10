"""
Django settings for SuperManager project.
"""

import os
from pathlib import Path
from collections import OrderedDict
from decouple import AutoConfig, RepositoryEnv
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if (os.path.isfile(BASE_DIR / '.env.development')):
    config = AutoConfig(search_path=BASE_DIR)
    config.SUPPORTED = OrderedDict([
        ('.env.development', RepositoryEnv),
    ])
    environment = 'development'
elif (os.path.isfile(BASE_DIR / '.env.testing')):
    config = AutoConfig(search_path=BASE_DIR)
    config.SUPPORTED = OrderedDict([
        ('.env.testing', RepositoryEnv),
    ])
    environment = 'testing'
else:
    from decouple import config
    environment = 'production'

# APP NAME
APP_NAME = os.environ.get('APP_NAME', 'SuperManager') if environment == 'production' else config('APP_NAME', default='SuperManager')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') if environment == 'production' else config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get('DEBUG')) if environment == 'production' else config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: define the correct hosts in production!
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('TOKEN_LIFETIME_MINUTES')) if environment == 'production' else config('TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('TOKEN_REFRESH_LIFETIME_DAYS')) if environment == 'production' else config('TOKEN_REFRESH_LIFETIME_DAYS', default=7, cast=int)),
    "TOKEN_OBTAIN_SERIALIZER": "api.serializers.AuthTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "api.serializers.AuthTokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "api.serializers.AuthTokenVerifySerializer",
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': os.environ.get('TOKEN_ALGORITHM') if environment == 'production' else config('TOKEN_ALGORITHM', default='HS256', cast=str),
    'SIGNING_KEY': os.environ.get('TOKEN_SIGNING_KEY') if environment == 'production' else config('TOKEN_SIGNING_KEY'),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Allowed hosts configuration
sm_allowed_hosts_check = os.environ.get('ALLOWED_HOSTS') if environment == 'production' else config('ALLOWED_HOSTS')
if sm_allowed_hosts_check == '*' or not sm_allowed_hosts_check:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = sm_allowed_hosts_check.split(',')

# Allowed CIDR networks configuration for AllowCIDRMiddleware
sm_allowed_cidr_nets_check = os.environ.get('ALLOWED_CIDR_NETS') if environment == 'production' else config('ALLOWED_CIDR_NETS')
if sm_allowed_cidr_nets_check == '*' or not sm_allowed_cidr_nets_check:
    ALLOWED_CIDR_NETS = ["0.0.0.0/0", "::/0"]
else:
    ALLOWED_CIDR_NETS = sm_allowed_cidr_nets_check.split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',
    'django_filters',
    'drf_yasg',
    'api'
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware',
]

# DRF configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': int(os.environ.get('PAGINATION_PAGE_SIZE')) if environment == 'production' else config('PAGINATION_PAGE_SIZE', default=10, cast=int),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_ORDERING_BACKENDS': ['rest_framework.filters.OrderingFilter'],
}
'''rest_framework.authentication.SessionAuthentication',''' # Optional for test browsable API

# URL configuration
ROOT_URLCONF = 'supermanager.urls'

# Templates configuration
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

# WSGI application
WSGI_APPLICATION = 'supermanager.wsgi.application'

# Database configuration
DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE') if environment == 'production' else config('DATABASE_ENGINE', default='', cast=str)

if DATABASE_ENGINE == 'django.db.backends.sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / (os.environ.get('DATABASE_NAME') if environment == 'production' else config('DATABASE_NAME', default='', cast=str)),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DATABASE_ENGINE,
            'NAME': os.environ.get('DATABASE_NAME') if environment == 'production' else config('DATABASE_NAME', default='', cast=str),
            'USER': os.environ.get('DATABASE_USER') if environment == 'production' else config('DATABASE_USER', default='', cast=str),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD') if environment == 'production' else config('DATABASE_PASSWORD', default='', cast=str),
            'HOST': os.environ.get('DATABASE_HOST') if environment == 'production' else config('DATABASE_HOST', default='', cast=str),
            'PORT': os.environ.get('DATABASE_PORT') if environment == 'production' else config('DATABASE_PORT', default='', cast=str),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Swagger settings
SWAGGER_USE_COMPAT_RENDERERS = False

# Frontend URL for password reset links
FRONTEND_URL = os.environ.get('FRONTEND_URL') if environment == 'production' else config('FRONTEND_URL', default='', cast=str)

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Media files (uploads)
MEDIA_URL = os.environ.get('MEDIA_URL') if environment == 'production' else config('MEDIA_URL', default='/media/', cast=str)
media_root_path = os.environ.get('MEDIA_ROOT') if environment == 'production' else config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'), cast=str)
MEDIA_ROOT = os.path.join(BASE_DIR, media_root_path)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_ENABLED = bool(os.environ.get('EMAIL_ENABLED')) if environment == 'production' else config('EMAIL_ENABLED', default=False, cast=bool)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND') if environment == 'production' else config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend', cast=str)
EMAIL_HOST = os.environ.get('EMAIL_HOST') if environment == 'production' else config('EMAIL_HOST', default='localhost', cast=str)
EMAIL_PORT = int(os.environ.get('EMAIL_PORT')) if environment == 'production' else config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USER = os.environ.get('EMAIL_USER') if environment == 'production' else config('EMAIL_USER', default='', cast=str)
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') if environment == 'production' else  config('EMAIL_PASSWORD', default='', cast=str)
EMAIL_USE_TLS = bool(os.environ.get('EMAIL_USE_TLS')) if environment == 'production' else config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = bool(os.environ.get('EMAIL_USE_SSL')) if environment == 'production' else config('EMAIL_USE_SSL', default=False, cast=bool)
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') if environment == 'production' else config('DEFAULT_FROM_EMAIL', default='webmaster@localhost', cast=str)

# Email settings for password reset
EMAIL_PWRESET_SUBJECT = os.environ.get('EMAIL_PWRESET_SUBJECT') if environment == 'production' else config('EMAIL_PWRESET_SUBJECT', default='[SuperManager] Password Reset', cast=str)
EMAIL_PWRESET_MESSAGE = os.environ.get('EMAIL_PWRESET_MESSAGE') if environment == 'production' else config('EMAIL_PWRESET_MESSAGE', default="Use this link to reset your password: {reset_url}", cast=str)
EMAIL_PWRESET_URL = os.environ.get('EMAIL_PWRESET_URL') if environment == 'production' else config('EMAIL_PWRESET_URL', default="{FRONTEND_URL}/auth/reset-password/{uid}/{token}", cast=str)
