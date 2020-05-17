"""
Django settings for safemasks project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured

from safemasks.safemasks.utils import parse_db_from_environ, parse_email_from_environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


SECRET_KEY = os.environ.get("SAFEMASKS_SECRET_KEY", None)

if SECRET_KEY is None:
    raise ImproperlyConfigured(
        "Could not infer 'SAFEMASKS_SECRET_KEY' from environment."
        " This key must be set in order for the app to work"
    )

ENVIRONMENT = os.environ.get("SAFEMASKS_ENVIRONMENT", None)
DEBUG = False
if ENVIRONMENT is None:
    raise ImproperlyConfigured(
        "Could not infer 'SAFEMASKS_ENVIRONMENT' from environment."
        " This key must be set in order for the app to work"
    )
DEBUG = ENVIRONMENT == "DEBUG"


ALLOWED_HOSTS = []
CURRENT_HOST = os.environ.get("SAFEMASKS_HOST", None)
if CURRENT_HOST:
    ALLOWED_HOSTS.append(CURRENT_HOST)

SITE_ID = 1


# Application definition
SAFEMASKS_APPS = ["safemasks.masks_auth", "safemasks.resources"]

EXTENSION_APPS = [
    "rest_framework",
    "bootstrap4",
    "crispy_forms",
]

INSTALLED_APPS = (
    SAFEMASKS_APPS
    + EXTENSION_APPS
    + [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "allauth",
        "allauth.account",
    ]
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "safemasks.safemasks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "safemasks", "templates"),
            os.path.join(BASE_DIR, "safemasks", "masks_auth", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "safemasks.safemasks.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {"default": parse_db_from_environ()}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True

## Crispy forms
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": ["safemasks.masks_auth.rest.permissions.IsReviewed"],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "UNICODE_JSON": False,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

## Authentification
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/profile/"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

# See also https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_BLACKLIST = []
ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_FORMS = {"signup": "safemasks.masks_auth.forms.SignupForm"}

## Email
_EMAIL_DATA = parse_email_from_environ()
DEFAULT_FROM_EMAIL = "no-reply@safemasks.de"
EMAIL_BACKEND = _EMAIL_DATA.get("EMAIL_BACKEND", None)
EMAIL_HOST = _EMAIL_DATA.get("EMAIL_HOST", None)
EMAIL_HOST_USER = _EMAIL_DATA.get("EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = _EMAIL_DATA.get("EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = _EMAIL_DATA.get("EMAIL_USE_TLS", None)
EMAIL_USE_SSL = _EMAIL_DATA.get("EMAIL_USE_SSL", None)
EMAIL_PORT = _EMAIL_DATA.get("EMAIL_PORT", None)
