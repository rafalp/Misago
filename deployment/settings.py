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

# Database connection
DATABASES = {
    'default': {
        'ENGINE': '',                    # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Cache engine
# Misago is EXTREMELY data hungry
# If you don't set any cache, it will BRUTALISE your database and memory
# In production ALWAYS use cache
CACHES = {}

# Cookies configuration
COOKIES_DOMAIN = '' # Set empty for automatic detection.
COOKIES_PATH = '' # Set empty for automatic detection.
COOKIES_PREFIX = '' # Allows you to avoid cookies collisions with other applications.
COOKIES_SECURE = False # Set this to true if AND ONLY IF you are using SSL on your forum.

# Sessions configuration
SESSION_LIFETIME = 86400 # Number of seconds since last request after which session is marked as expired.

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
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
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
    '',
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
    '/templates'
)

# List of installed themes
INSTALLED_THEMES = (
    'sora',  # Default style always first
    'admin', # Admin theme always last
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'deployment.wsgi.application'
