import os

# Board address
BOARD_ADDRESS = 'http://127.0.0.1:8000/'

# Admin control panel path
# Leave this setting empty
ADMIN_PATH = ''

# Default format of Misago generated HTML
OUTPUT_FORMAT = 'html5'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of directories that contain Misago locale files
# Defautly set Django to look for Misago translations in misago/locale directory
LOCALE_PATHS = (
    ('%slocale%s' % (os.path.dirname( __file__ ) + os.sep, os.sep)),
)

# Catch-all e-mail address
# If DEBUG_MODE is on, all emails will be sent to this address instead of real recipient.
CATCH_ALL_EMAIL_ADDRESS = ''

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'misago.context_processors.core',
    'misago.admin.context_processors.admin',
    'misago.banning.context_processors.banning',
    'misago.messages.context_processors.messages',
    'misago.monitor.context_processors.monitor',
    'misago.settings.context_processors.settings',
    'misago.bruteforce.context_processors.is_jammed',
    'misago.csrf.context_processors.csrf',
    'misago.users.context_processors.user',
)

# Jinja2 Template Extensions
JINJA2_EXTENSIONS = (
    'jinja2.ext.do',
)

# List of application middlewares
MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'misago.cookie_jar.middleware.CookieJarMiddleware',
    'misago.settings.middleware.SettingsMiddleware',
    'misago.monitor.middleware.MonitorMiddleware',
    'misago.themes.middleware.ThemeMiddleware',
    'misago.firewalls.middleware.FirewallMiddleware',
    'misago.crawlers.middleware.DetectCrawlerMiddleware',
    'misago.sessions.middleware.SessionMiddleware',
    'misago.bruteforce.middleware.JamMiddleware',
    'misago.csrf.middleware.CSRFMiddleware',
    'misago.banning.middleware.BanningMiddleware',
    'misago.messages.middleware.MessagesMiddleware',
    'misago.users.middleware.UserMiddleware',
    'misago.acl.middleware.ACLMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# List of application permission providers
PERMISSION_PROVIDERS = (
    'misago.usercp.acl',
    'misago.admin.acl',
)

# Name of root urls configuration
ROOT_URLCONF = 'misago.urls'

#Installed applications
INSTALLED_APPS = (
    # Applications that have no dependencies first!
    'south',
    'coffin',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mptt', # Modified Pre-order Tree Transversal - allows us to nest forums 
    'debug_toolbar', # Debug toolbar
    'misago.acl', # ACL Builder and dehydrator
    'misago.settings', # Database level application configuration
    'misago.monitor', # Forum statistics monitor
    'misago.utils', # Utility classes
    # Applications with dependencies
    'misago.banning', # Banning and blacklisting users
    'misago.crawlers', # Web crawlers handling
    'misago.cookie_jar', # Cookies helper
    'misago.captcha', # Web crawlers handling
    'misago.forums', # Forums, threads and posts
    'misago.messages', # Messages and Flashes
    'misago.newsletters', # Send newsletters to members from Admin
    'misago.stats', # Admin statistics generator
    'misago.sessions', # Sessions
    'misago.authn', # User authentication
    'misago.bruteforce', # Brute-Force protection
    'misago.csrf', # Cross Site Request Forgery protection
    'misago.setup', # Installation/update tool
    'misago.template', # Templates extensions
    'misago.themes', # Themes
    'misago.users', # Users foundation
    'misago.prune', # Prune Users
    'misago.ranks', # User Ranks
    'misago.roles', # User Roles
    'misago.usercp', # User Control Panel
    'misago.profiles', # User Profiles
    'misago.register', # Register New Users
    'misago.activation', # Activate inactive User or resend activation e-mail
    'misago.resetpswd', # Reset User Password
)

# IP's that can see debug toolbar
INTERNAL_IPS = ('127.0.0.1', '::1')

# Debug toolbar config
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False
}

# List panels displayed by toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'debug_toolbar.panels.version.VersionDebugPanel',
)

# Turn off caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
