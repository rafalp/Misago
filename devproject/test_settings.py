from .settings import *  # pylint: disable-all

# Use in-memory cache
CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}

# Disable Celery backend
CELERY_BROKER_URL = None

# Disable Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {}
INTERNAL_IPS = []

# Store mails in memory
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Disable account validation via Stop Forum Spam
MISAGO_NEW_REGISTRATIONS_VALIDATORS = ("misago.users.validators.validate_gmail_email",)

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

# Use Django's redirects for serving attachments
MISAGO_ATTACHMENTS_SERVER = "misago.attachments.servers.django_redirect_response"

# Use english search config
MISAGO_SEARCH_CONFIG = "english"

# Test assertions expect english locale
LANGUAGE_CODE = "en-us"

# Test assertions expect specific TZ
TIME_ZONE = "UTC"

# Register test post validator
MISAGO_POST_VALIDATORS = ["misago.core.testproject.validators.test_post_validator"]

# Register test post search filter
MISAGO_POST_SEARCH_FILTERS = ["misago.core.testproject.searchfilters.test_filter"]

# Default test name
TEST_NAME = "miasago_test"
