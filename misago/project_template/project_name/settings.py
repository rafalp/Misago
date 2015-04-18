"""
Misago settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

# Import Misago defaults for overriding
from misago.conf.defaults import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

# Hosts allowed to POST to your site
# If you are unsure, just enter here your host name, eg. 'mysite.com'

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Cache
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


# Site language
# https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

LANGUAGE_CODE = 'en-us'


# Path used to access static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'

# Path used to access uploaded media (Avatars and Profile Backgrounds, ect.)
# This is NOT path used to serve posts attachments.
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/
MEDIA_URL = '/media/'


# Automatically setup default paths to media and attachments directories
MISAGO_ATTACHMENTS_ROOT = os.path.join(BASE_DIR, 'attachments')
MISAGO_AVATAR_STORE = os.path.join(BASE_DIR, 'avatar_store')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Automatically setup default paths for static and template directories
# You can use those directories to easily customize and add your own
# assets and templates to your site
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'theme/static'),
) + STATICFILES_DIRS

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'theme/templates'),
) + TEMPLATE_DIRS


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'


# X-Sendfile support
# X-Sendfile is feature provided by Http servers that allows web apps to
# delegate serving files over to the better performing server instead of
# doing it within app.
# If your server supports X-Sendfile or its variation, enter header name here.
# For example if you are using Nginx with X-accel enabled, set this setting
# to "X-Accel-Redirect".
# Leave this setting empty to Django fallback instead
MISAGO_SENDFILE_HEADER = ''

# Allows you to use location feature of your Http server
# For example, if you have internal location /mymisago/avatar_cache/
# that points at /home/myweb/misagoforum/avatar_cache/, set this setting
# to "mymisago".
MISAGO_SENDFILE_LOCATIONS_PATH = ''


# Application definition
# Don't edit those settings unless you know what you are doing
ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
