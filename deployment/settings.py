import sys
from misago.settings_base import *

# Allow debug?
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Board address
BOARD_ADDRESS = 'http://somewhere.com'

# Admin control panel path
# Leave this setting empty or remove it to turn admin panel off.
# Misago always asserts that it has correct admin path and fixes it
# if neccessary. This means "/admincp////" becomes "admincp/" and
# "administration" becomes "administration/"
ADMIN_PATH = 'admincp'

# System admins
ADMINS = ()

# Secret key is used by Django and Misago in hashes generation
# YOU MUST REPLACE IT with random combination of characters
# NEVER EVER SHARE THIS KEY WITH ANYBODY!
# Make it messed up and long, this is example of good secret key:
# yaobeifl1a6hf&3)^uc#^vlu1ud7xp^+*c5zoq*tf)fvs#*o$#
SECRET_KEY = 'secret-key'

# Database connection
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Can be either 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database.db', # Name of the database or the path to the database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Cache engine
# Misago is EXTREMELY data hungry
# If you don't set any cache, it will BRUTALISE your database and memory
# In production ALWAYS use cache
# For reference read following document:
# https://docs.djangoproject.com/en/dev/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Cookies configuration
COOKIES_DOMAIN = '192.168.33.10' # E.g. a cookie domain for "www.mysite.com" or "forum.mysite.com" is ".mysite.com"
COOKIES_PATH = '/'
COOKIES_PREFIX = '' # Allows you to avoid cookies collisions with other applications.
COOKIES_SECURE = False # Set this to true if, AND ONLY IF, you are using SSL on your forum.

# Sessions configuration
SESSION_LIFETIME = 3600 # Number of seconds since last request after which session is marked as expired.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en_US'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Always use forward slashes, even on Windows.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/vagrant/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# Always use forward slashes, even on Windows.
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Make sure directory containing avatars is located under first directory on list
    '/vagrant/static/',
)

# E-mail host
EMAIL_HOST = ''

# E-mail port
EMAIL_PORT = 25

# E-mail host user
EMAIL_HOST_USER = ''

# E-mail host password
EMAIL_HOST_PASSWORD = ''

# Use TLS encryption
EMAIL_USE_TLS = False

# E-mail subject prefix added to emails for staff
EMAIL_SUBJECT_PREFIX = '[Misago]'

# Catch-all e-mail address
# If DEBUG_MODE is on, all emails will be sent to this address instead of real recipient.
CATCH_ALL_EMAIL_ADDRESS = ''

# Directories with templates
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/vagrant/templates'
)

# List of installed themes
INSTALLED_THEMES = (
    'cranefly', # Default style always first
    'admin', # Admin theme always last
)

# Enable mobile subdomain for mobile stuff
MOBILE_SUBDOMAIN = ''

# Templates used by mobile version
MOBILE_TEMPLATES = ''

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deployment.wsgi.application'

# Empty secret key if its known
if SECRET_KEY == 'yaobeifl1a6hf&3)^uc#^vlu1ud7xp^+*c5zoq*tf)fvs#*o$#':
    SECRET_KEY = ''

# Override config if we are in tests
if 'test' in sys.argv:
    if not SECRET_KEY:
        SECRET_KEY = 'SECRET4TESTS'
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db4testing'}
    CACHES['default'] = {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    SKIP_SOUTH_TESTS = True
    MEDIA_URL = "http://media.domain.com/"