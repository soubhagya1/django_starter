from .base import *

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# but now:

# no PostgreSQL dependency
# no Redis dependency
# no Celery dependency

# Tests become much faster.
# now in ci cd pipeline we can run tests without needing to set up PostgreSQL, Redis and Celery, which makes it faster and easier to run tests in ci cd pipeline.
