"""
Misago default settings

This fille sets everything Misago needs to run.

If you want to add custom app, middleware or path, please update setting vallue
defined in this file instead of copying setting from here to your settings.py.

Yes:

#yourproject/settings.py
INSTALLED_APPS += (
    'myawesomeapp',
)

No:

#yourproject/settings.py
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'misago.core',
    'misago.conf',
    ...
    'myawesomeapp',
)
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
MISAGO_BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Assets Pipeline
# See http://django-pipeline.readthedocs.org/en/latest/configuration.html

PIPELINE_CSS = {
    'misago': {
        'source_filenames': (
            'misago/css/style.less',
        ),
        'output_filename': 'misago.css',
    },
    'misago_admin': {
        'source_filenames': (
            'misago/admin/css/style.less',
        ),
        'output_filename': 'misago_admin.css',
    },
}

PIPELINE_JS = {
    'misago': {
        'source_filenames': (
            'misago/js/jquery.js',
            'misago/js/bootstrap.js',
        ),
        'output_filename': 'misago.js',
    },
    'misago_admin': {
        'source_filenames': (
            'misago/admin/js/jquery.js',
            'misago/admin/js/bootstrap.js',
            'misago/admin/js/misago-tooltips.js',
            'misago/admin/js/misago-tables.js',
            'misago/admin/js/misago-yesnoswitch.js',
        ),
        'output_filename': 'misago_admin.js',
    },
}

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'south',
    'pipeline',
    'crispy_forms',
    'mptt',
    'misago.admin',
    'misago.acl',
    'misago.core',
    'misago.conf',
    'misago.users',
    'misago.faker',
    'misago.forums',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'misago.core.middleware.threadstore.ThreadStoreMiddleware',
    'misago.core.middleware.exceptionhandler.ExceptionHandlerMiddleware',
    'misago.admin.middleware.AdminAuthMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'misago.core.context_processors.site_address',
    'misago.conf.context_processors.settings',
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

TIME_ZONE = 'UTC'


# Use Misago CSRF Failure Page
CSRF_FAILURE_VIEW = 'misago.core.errorpages.csrf_failure'


# Use Misago authentication
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'misago.users.authbackends.MisagoBackend',
)

# How many e-mails should be sent in single step.
# This is used for conserving memory usage when mailing many users at same time

MISAGO_MAILER_BATCH_SIZE = 20

# Auth paths
LOGIN_REDIRECT_URL = 'misago:index'
LOGIN_URL = 'misago:login'
LOGOUT_URL = 'misago:logout'

# Misago Admin Path
# Omit starting and trailing slashes
# To disable Misago admin, empty this value
MISAGO_ADMIN_PATH = 'admincp'

# Admin urls namespaces that Misago's AdminAuthMiddleware should protect
MISAGO_ADMIN_NAMESPACES = (
    'admin',
    'misago:admin',
)

# How long (in minutes) since previous request to admin namespace should
# admin session last.
MISAGO_ADMIN_SESSION_EXPIRATION = 60


# Default forms templates
CRISPY_TEMPLATE_PACK = 'bootstrap3'
