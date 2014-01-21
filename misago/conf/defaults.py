"""
Misago default settings

You are strongly advised to import this file at the top of your project's settings.py
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
MISAGO_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'misago.core',
    'misago.conf',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Register Misago directories

LOCALE_PATHS = (
    os.path.join(MISAGO_BASE_DIR, 'locale'),
)

STATICFILES_DIRS = (
    os.path.join(MISAGO_BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(MISAGO_BASE_DIR, 'templates'),
)


# Internationalization

USE_I18N = True

USE_L10N = True

USE_TZ = True