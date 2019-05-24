import os

from .settings import *  # pylint: disable-all

# Use test DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_TEST_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": 5432,
    }
}

# Use in-memory cache
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# Disable Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {}
INTERNAL_IPS = []

# Disable account validation via Stop Forum Spam
MISAGO_NEW_REGISTRATIONS_VALIDATORS = ("misago.users.validators.validate_gmail_email",)

# Store mails in memory
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Use MD5 password hashing to speed up test suite
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Simplify password validation to ease writing test assertions
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ["username", "email"]},
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 7},
    },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Use english search config
MISAGO_SEARCH_CONFIG = "english"

# Register test post validator
MISAGO_POST_VALIDATORS = ["misago.core.testproject.validators.test_post_validator"]

# Register test post search filter
MISAGO_POST_SEARCH_FILTERS = ["misago.core.testproject.searchfilters.test_filter"]

# Additional overrides for Travis-CI
if os.environ.get("TRAVIS"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "travis_ci_test",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "127.0.0.1",
            "PORT": "",
        }
    }

    TEST_NAME = "travis_ci_test"
