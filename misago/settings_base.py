import os

# Board address
BOARD_ADDRESS = 'http://127.0.0.1:8000/'

# Allowed hosts
ALLOWED_HOSTS = ['*']

# Admin control panel path
# Leave this setting empty
ADMIN_PATH = ''

# Default format of Misago generated HTML
OUTPUT_FORMAT = 'html5'

# Default avatar sizes
# Those are avatar sizes Misago generates images for
# Remember to run "genavatars" command when you change this setting!
AVATAR_SIZES = (125, 100, 80, 60, 40, 24)

# Allow usernames to contain diacritics
UNICODE_USERNAMES = True

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
    ('%slocale%s' % (os.path.dirname(__file__) + os.sep, os.sep)),
)

# Catch-all e-mail address
# If DEBUG_MODE is on, all emails will be sent to this address instead of real recipient.
CATCH_ALL_EMAIL_ADDRESS = ''

# Forums and threads read tracker length (days
# Enter 0 to turn tracking off
# The bigger the number, then longer tracker keeps threads reads
# information and the more costful it is to track reads
READS_TRACKER_LENGTH = 7

# Heartbeat Path for crons
# Use this path if you wish to keep Misago alive using separate cron
# By quering this path from your cron you'll keep Misago's base clean
# Leave empty if you don't use Heartbeat cron
HEARTBEAT_PATH = ''

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
    'misago.context_processors.common',
    'misago.context_processors.admin',
)

# Jinja2 Template Extensions
JINJA2_EXTENSIONS = (
    'jinja2.ext.do',
)

# List of application middlewares
MIDDLEWARE_CLASSES = (
    'misago.stopwatch.middleware.StopwatchMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'misago.heartbeat.middleware.HeartbeatMiddleware',
    'misago.middleware.cookiejar.CookieJarMiddleware',
    'misago.middleware.settings.SettingsMiddleware',
    'misago.middleware.monitor.MonitorMiddleware',
    'misago.middleware.theme.ThemeMiddleware',
    'misago.middleware.firewalls.FirewallMiddleware',
    'misago.middleware.crawlers.DetectCrawlerMiddleware',
    'misago.middleware.session.SessionMiddleware',
    'misago.middleware.bruteforce.JamMiddleware',
    'misago.middleware.csrf.CSRFMiddleware',
    'misago.middleware.banning.BanningMiddleware',
    'misago.middleware.messages.MessagesMiddleware',
    'misago.middleware.users.UserMiddleware',
    'misago.middleware.acl.ACLMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# List of application permission providers
PERMISSION_PROVIDERS = (
    'misago.usercp.acl',
    'misago.users.acl',
    'misago.admin.acl',
    'misago.forums.acl',
    'misago.threads.acl',
)

# List of UserCP extensions
USERCP_EXTENSIONS = (
    'misago.usercp.options',
    'misago.usercp.avatar',
    'misago.usercp.signature',
    'misago.usercp.credentials',
    'misago.usercp.username',
)

# List of User Profile extensions
PROFILE_EXTENSIONS = (
    'misago.profiles.posts',
    'misago.profiles.threads',
    'misago.profiles.follows',
    'misago.profiles.followers',
    'misago.profiles.details',
)

# List of Markdown Extensions
MARKDOWN_EXTENSIONS = (
    'misago.markdown.extensions.quotes.QuoteTitlesExtension',
    'misago.markdown.extensions.mentions.MentionsExtension',
    'misago.markdown.extensions.magiclinks.MagicLinksExtension',
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
    'misago', # Misago Forum App
)

# Stopwatch target file
STOPWATCH_LOG = ''

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
    #'misago.acl.panels.MisagoACLDebugPanel',
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

# Create copy of installed apps list
# South overrides INSTALLED_APPS list with custom one
# that doesn't contain apps without models when it
# runs its own syncdb
# Misago's loaddata command requires complete list of
# installed apps in order to work correctly
import copy
INSTALLED_APPS_COMPLETE = copy.copy(INSTALLED_APPS)
