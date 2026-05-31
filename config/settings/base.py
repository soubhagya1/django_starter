from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
from celery.schedules import crontab

DEBUG = os.getenv("DEBUG") == "1"

TIME_ZONE = "Asia/Kolkata"
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

ROOT_URLCONF = "config.urls"

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True

# STATIC_URL = '/static/'
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # for production
STATICFILES_DIRS = [BASE_DIR / "static"]  # for development

# ALLOWED_HOSTS = []
# ALLOWED_HOSTS = [
#     "localhost",
#     "127.0.0.1",
# ]
# for docker, we need to allow all hosts or specify the docker network host
ALLOWED_HOSTS = ["*"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",  # /products?min_price=100&max_price=500
    "apps.accounts",
    # "apps.core",
    "apps.rbac",
    "apps.products",
    # "django_celery_beat",
    # 'rest_framework.authtoken',
    # 'core',
    # 'api',
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",  # for token blacklisting
]
INSTALLED_APPS += ["django_celery_beat"]

AUTH_USER_MODEL = "accounts.User"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # 'NAME': BASE_DIR / 'db.sqlite3',
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        # 'PORT': os.getenv('DB_PORT'),
        "PORT": os.getenv("DB_PORT", "5432"),
        # "OPTIONS": {"options": "-c timezone=Asia/Kolkata"},
    }
}

CACHES = {
    # "default": {
    #     # "BACKEND": "django_redis.cache.RedisCache",
    #     "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #     "LOCATION": os.getenv("REDIS_URL"),
    #     # "OPTIONS": {
    #     #     "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     # }
    # }
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "BACKEND": "django.core.cache.backends.locmem.LocMemCache", for testing without redis
        # "LOCATION": "redis://127.0.0.1:6379/1", #not for production or docker, use env variable
        "LOCATION": os.getenv(
            "REDIS_URL"
        ),  # above is localhost for local testing, for docker use env variable which is set to redis://redis:6379/1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BROKER_URL = os.getenv("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"

# CELERY_BROKER_URL = "redis://127.0.0.1:6379/1"
# CELERY_ACCEPT_CONTENT = ["json"]
# CELERY_TASK_SERIALIZER = "json"

CELERY_BEAT_SCHEDULE = {
    "daily-report": {
        "task": "apps.products.tasks.daily_product_report",
        # "schedule": crontab(hour=0, minute=0),  # every day midnight
        "schedule": crontab(minute="*"),  # for testing every minute
    },
}

# CELERY_BEAT_SCHEDULE = {
#     "test-every-minute": {
#         "task": "apps.products.tasks.test_scheduler",
#         "schedule": crontab(minute="*"),
#     },
# }

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # Every API requires JWT token, Session auth won’t be used for APIs
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),  # Every API requires login, No token → ❌ Unauthorized ,you can change to AllowAny for public access
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "EXCEPTION_HANDLER": "apps.core.exceptions.handler.custom_exception_handler",
    # "DEFAULT_THROTTLE_CLASSES": [
    #     "rest_framework.throttling.UserRateThrottle",
    #     "rest_framework.throttling.AnonRateThrottle",
    #     # "rest_framework.throttling.ScopedRateThrottle",
    # ],
    # "DEFAULT_THROTTLE_RATES": {
    #     "user": "2/min",
    #     "anon": "1/min",
    #     # "anon": "100/min",
    #     # "user": "1000/min",
    #     # 'login': '5/min',
    #     # 'products_list': '2/min',
    #     # 'products_create': '4/min',
    # },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD")

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

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# SPECTACULAR_SETTINGS = {
#     "TITLE": "Django Enterprise Backend API",
#     "DESCRIPTION": "Production-oriented Django REST backend",
#     "VERSION": "1.0.0",
# }
SPECTACULAR_SETTINGS = {
    "TITLE": "Product Management API",
    "VERSION": "v1",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
# LOGGING = {
#     "version": 1,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#         },
#     },
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/app.log"),
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

WSGI_APPLICATION = "config.wsgi.application"
