import os
import sys
from datetime import timedelta
from pathlib import Path

from .spectacular_settings import *

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("secretKeyDjango")

if SECRET_KEY:
    DEBUG = os.environ.get("debugMode")
    ALLOWED_HOSTS = [os.environ.get("allowedHosts")]
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("bdEngine"),
            "NAME": os.environ.get("bdName"),
            "USER": os.environ.get("bdUser"),
            "PASSWORD": os.environ.get("bdPass"),
            "HOST": os.environ.get("bdHost"),
            "PORT": os.environ.get("bdPort"),
        }
    }
    signingKey = os.environ.get("secretKeyJWT")

else:
    from .env import *

    SECRET_KEY = secretKeyDjango
    DEBUG = debug
    ALLOWED_HOSTS = allowedHosts
    DATABASES = {
        "default": {
            "ENGINE": bdEngine,
            "NAME": bdName,
            "USER": bdUser,
            "PASSWORD": bdPass,
            "HOST": bdHost,
            "PORT": bdPort,
        }
    }
    signingKey = secretKeyJWT

INTERNAL_IPS = [
    "127.0.0.1",
    "https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com/",
]

if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

CORS_ORIGIN_WHITELIST = [
    "https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOWED_HOSTS = [
    "https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://web-72ljjv9mgqrj.up-de-fra1-k8s-1.apps.run-on-seenode.com",
    "https://cloud.seenode.com",
    "http://127.0.0.1",
    "https://127.0.0.1",
]

CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "debug_toolbar",
    "maingigapizza",
    "admingigapizza",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

ROOT_URLCONF = "backendgigapizza.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backendgigapizza.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_REDIRECT_URL = "/redirect/"

SESSION_COOKIE_AGE = 1800

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

AUTH_USER_MODEL = "maingigapizza.Users"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DATE_INPUT_FORMATS": ["%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"],
    "TIME_INPUT_FORMATS": [
        "%H:%M",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=240),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": signingKey,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
