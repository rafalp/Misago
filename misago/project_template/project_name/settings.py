"""
Misago settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from misago.conf.defaults import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts allowed to POST to your site
# If you are unsure, just enter here your host name, eg. 'mysite.com'

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases

DATABASES = {
    'default': {
        # Only PostgreSQL is supported
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# PostgreSQL text search configuration to use in searches
# Defaults to "simple", for list of installed configurations run "\dF" in "psql"
# Standard configs as of PostgreSQL 9.5: dutch, english, finnish, french,
# german, hungarian, italian, norwegian, portuguese, romanian, russian, simple,
# spanish, swedish, turkish
# Example on adding custom language can be found here: https://github.com/lemonskyjwt/plpstgrssearch

MISAGO_SEARCH_CONFIG = 'simple'


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

# Fallback Timezone
# Used to format dates on server, that are then
# presented to clients with disabled JS
# Consult http://en.wikipedia.org/wiki/List_of_tz_database_time_zones TZ column
# for valid values

TIME_ZONE = 'UTC'


# Path used to access static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

STATIC_URL = '/static/'

# Path used to access uploaded media (Avatars and Profile Backgrounds, ect.)
# This is NOT path used to serve posts attachments.
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/
MEDIA_URL = '/media/'


# Automatically setup default paths to media and static directories
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Automatically setup default paths for static and template directories
# You can use those directories to easily customize and add your own
# assets and templates to your site
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'theme', 'static'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'theme', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': DEFAULT_CONTEXT_PROCESSORS,
        },
    },
]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '{{ secret_key }}'


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command
MISAGO_AVATAR_GALLERY = os.path.join(BASE_DIR, 'avatargallery')


# Application definition
# Don't edit those settings unless you know what you are doing
ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'
