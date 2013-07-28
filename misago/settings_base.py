import os

# Board address
BOARD_ADDRESS = 'http://127.0.0.1:8000/'

# Allowed hosts
ALLOWED_HOSTS = ['*']

# Admin control panel path
# Leave this setting empty
ADMIN_PATH = ''

# Enable mobile subdomain for mobile stuff
MOBILE_SUBDOMAIN = ''

# Templates used by mobile version
MOBILE_TEMPLATES = ''

# Default format of Misago generated HTML
OUTPUT_FORMAT = 'html5'

# Default avatar sizes
# Those are avatar sizes Misago generates images for
# Remember to run "genavatars" command when you change this setting!
AVATAR_SIZES = (125, 100, 80, 60, 40, 24)

# Allow usernames to contain diacritics
UNICODE_USERNAMES = True

# Default anti-flood delay (seconds)
FLOOD_DELAY = 35

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

# Forums and threads read tracker length (days)
# Enter 0 to turn tracking off
# The bigger the number, then longer tracker keeps threads reads
# information and the more costful it is to track reads
READS_TRACKER_LENGTH = 7

# Min. number of days between synchronisating member profiles
# Allows you to keep your member profiles up to date, enter 0 to never sync
PROFILES_SYNC_FREQUENCY = 7

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
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)

# Template extensions that will cause Jinja2 to be used
DEFAULT_JINJA2_TEMPLATE_EXTENSION = ('.html', '.txt')

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

# Template middlewares
TEMPLATE_MIDDLEWARES = ()

# Jinja2 Template Extensions
JINJA2_EXTENSIONS = (
    'jinja2.ext.do',
)

# List of application middlewares
MIDDLEWARE_CLASSES = (
    'misago.middleware.thread.ThreadMiddleware',
    'misago.middleware.stopwatch.StopwatchMiddleware',
    'misago.middleware.heartbeat.HeartbeatMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'misago.middleware.cookiejar.CookieJarMiddleware',
    'misago.middleware.theme.ThemeMiddleware',
    'misago.middleware.firewalls.FirewallMiddleware',
    'misago.middleware.crawlers.DetectCrawlerMiddleware',
    'misago.middleware.session.SessionMiddleware',
    'misago.middleware.bruteforce.JamMiddleware',
    'misago.middleware.csrf.CSRFMiddleware',
    'misago.middleware.banning.BanningMiddleware',
    'misago.middleware.messages.MessagesMiddleware',
    'misago.middleware.user.UserMiddleware',
    'misago.middleware.mailsqueue.MailsQueueMiddleware',
    'misago.middleware.acl.ACLMiddleware',
    'misago.middleware.privatethreads.PrivateThreadsMiddleware',
    'django.middleware.common.CommonMiddleware',
)

# List of application permission providers
PERMISSION_PROVIDERS = (
    'misago.acl.permissions.usercp',
    'misago.acl.permissions.search',
    'misago.acl.permissions.users',
    'misago.acl.permissions.forums',
    'misago.acl.permissions.threads',
    'misago.acl.permissions.privatethreads',
    'misago.acl.permissions.reports',
    'misago.acl.permissions.special',
)

# List of UserCP extensions
USERCP_EXTENSIONS = (
    'misago.apps.usercp.options',
    'misago.apps.usercp.avatar',
    'misago.apps.usercp.signature',
    'misago.apps.usercp.credentials',
    'misago.apps.usercp.username',
)

# List of User Profile extensions
PROFILE_EXTENSIONS = (
    'misago.apps.profiles.posts',
    'misago.apps.profiles.threads',
    'misago.apps.profiles.follows',
    'misago.apps.profiles.followers',
    'misago.apps.profiles.details',
)

# List of User Model relations that should be loaded by session handler
USER_EXTENSIONS_PRELOAD = ()

# List of User Model relations that should be loaded when displaying users profiles
PROFILE_EXTENSIONS_PRELOAD = ()

# List of Markdown Extensions
MARKDOWN_EXTENSIONS = (
    'misago.markdown.extensions.strikethrough.StrikethroughExtension',
    'misago.markdown.extensions.quotes.QuoteTitlesExtension',
    'misago.markdown.extensions.mentions.MentionsExtension',
    'misago.markdown.extensions.magiclinks.MagicLinksExtension',
    'misago.markdown.extensions.cleanlinks.CleanLinksExtension',
    'misago.markdown.extensions.shorthandimgs.ShorthandImagesExtension',
    # Uncomment for EXPERIMENTAL BBCode support
    #'misago.markdown.extensions.bbcodes.BBCodesExtension',
    # Uncomment for emoji support, requires emoji directory in static dir.
    #'misago.markdown.extensions.emoji.EmojiExtension',
)

# Name of root urls configuration
ROOT_URLCONF = 'misago.urls'

#Installed applications
INSTALLED_APPS = (
    # Applications that have no dependencies first!
    'south', # Database schema building and updating
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_jinja', # Jinja2 integration
    'django_jinja.contrib._humanize', # Some Django filters
    'floppyforms', # Better forms
    'mptt', # Modified Pre-order Tree Transversal - allows us to nest forums
    'haystack', # Search engines bridge
    'debug_toolbar', # Debug toolbar'
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
    'misago.acl.panels.MisagoACLDebugPanel',
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
