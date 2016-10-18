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

# Build paths inside the project like this: os.path.join(MISAGO_BASE_DIR, ...)
import os


MISAGO_BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Default JS debug to false
# This setting used exclusively by test runner and isn't part of public API
_MISAGO_JS_DEBUG = False


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    # Keep misago.users above django.contrib.auth
    # so our management commands take precedence over theirs
    'misago.users',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'debug_toolbar',
    'crispy_forms',
    'mptt',
    'rest_framework',
    'misago.admin',
    'misago.acl',
    'misago.core',
    'misago.conf',
    'misago.markup',
    'misago.legal',
    'misago.categories',
    'misago.threads',
    'misago.readtracker',
    'misago.faker',
)

MIDDLEWARE_CLASSES = (
    'misago.users.middleware.AvatarServerMiddleware',
    'misago.users.middleware.RealIPMiddleware',
    'misago.core.middleware.frontendcontext.FrontendContextMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'misago.users.middleware.UserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'misago.core.middleware.exceptionhandler.ExceptionHandlerMiddleware',
    'misago.users.middleware.OnlineTrackerMiddleware',
    'misago.admin.middleware.AdminAuthMiddleware',
    'misago.threads.middleware.UnreadThreadsCountMiddleware',
    'misago.core.middleware.threadstore.ThreadStoreMiddleware',
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
    'misago.users.context_processors.user_links',
    'misago.legal.context_processors.legal_links',

    # Data preloaders
    'misago.conf.context_processors.preload_settings_json',
    'misago.markup.context_processors.preload_api_url',
    'misago.threads.context_processors.preload_threads_urls',
    'misago.users.context_processors.preload_user_json',

    # Note: keep frontend_context processor last for previous processors
    # to be able to add data to request.frontend_context
    'misago.core.context_processors.frontend_context',
)

MISAGO_ACL_EXTENSIONS = (
    'misago.users.permissions.account',
    'misago.users.permissions.profiles',
    'misago.users.permissions.warnings',
    'misago.users.permissions.moderation',
    'misago.users.permissions.delete',
    'misago.categories.permissions',
    'misago.threads.permissions.attachments',
    'misago.threads.permissions.threads',
    'misago.threads.permissions.privatethreads',
)

MISAGO_MARKUP_EXTENSIONS = ()

MISAGO_POSTING_MIDDLEWARES = (
    # Note: always keep FloodProtectionMiddleware middleware first one
    'misago.threads.api.postingendpoint.floodprotection.FloodProtectionMiddleware',
    'misago.threads.api.postingendpoint.category.CategoryMiddleware',
    'misago.threads.api.postingendpoint.reply.ReplyMiddleware',
    # 'misago.threads.api.postingendpoint.participants.ThreadParticipantsFormMiddleware',
    'misago.threads.api.postingendpoint.pin.PinMiddleware',
    'misago.threads.api.postingendpoint.close.CloseMiddleware',
    'misago.threads.api.postingendpoint.hide.HideMiddleware',
    'misago.threads.api.postingendpoint.protect.ProtectMiddleware',
    # 'misago.threads.api.postingendpoint.recordedit.RecordEditMiddleware',
    'misago.threads.api.postingendpoint.updatestats.UpdateStatsMiddleware',
    'misago.threads.api.postingendpoint.mentions.MentionsMiddleware',
    'misago.threads.api.postingendpoint.subscribe.SubscribeMiddleware',
    # Note: always keep SaveChangesMiddleware middleware after all state-changing middlewares
    'misago.threads.api.postingendpoint.savechanges.SaveChangesMiddleware',
    # Those middlewares are last because they don't change app state
    'misago.threads.api.postingendpoint.emailnotification.EmailNotificationMiddleware',
)

MISAGO_THREAD_TYPES = (
    'misago.threads.threadtypes.thread.Thread',
    'misago.threads.threadtypes.privatethread.PrivateThread',
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


# Misago specific date formats
# https://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH = 'j M'
MISAGO_COMPACT_DATE_FORMAT_DAY_MONTH_YEAR = 'M \'y'


# Use Misago CSRF Failure Page
CSRF_FAILURE_VIEW = 'misago.core.errorpages.csrf_failure'


# Use Misago authentication
AUTH_USER_MODEL = 'misago_users.User'

AUTHENTICATION_BACKENDS = (
    'misago.users.authbackends.MisagoBackend',
)

MISAGO_NEW_REGISTRATIONS_VALIDATORS = (
    'misago.users.validators.validate_gmail_email',
    'misago.users.validators.validate_with_sfs',
)

MISAGO_STOP_FORUM_SPAM_USE = True
MISAGO_STOP_FORUM_SPAM_MIN_CONFIDENCE = 80


# How many e-mails should be sent in single step.
# This is used for conserving memory usage when mailing many users at same time

MISAGO_MAILER_BATCH_SIZE = 20

# Auth paths
MISAGO_LOGIN_API_URL = 'auth'

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


# Display threads on forum index
# Change this to false to display categories list instead
MISAGO_THREADS_ON_INDEX = True


# Max age of notifications in days
# Notifications older than this are deleted
# On very active forums its better to keep this smaller
MISAGO_NOTIFICATIONS_MAX_AGE = 40


# Fail-safe limits in case forum is raided by spambot
# No user may exceed those limits, however you may disable
# them by changing them to 0
MISAGO_DIALY_POST_LIMIT = 600
MISAGO_HOURLY_POST_LIMIT = 100


# Function used for generating individual avatar for user
MISAGO_DYNAMIC_AVATAR_DRAWER = 'misago.users.avatars.dynamic.draw_default'

# For which sizes avatars should be cached
# Keep sizes ordered from greatest to smallest
# Max size also controls min size of uploaded image as well as crop size
MISAGO_AVATARS_SIZES = (400, 200, 150, 100, 64, 50, 30, 20)

# Path to avatar server
# This path is used to detect avatar requests, which bypass most of
# Request/Response processing for performance reasons
MISAGO_AVATAR_SERVER_PATH = '/user-avatar'


# Number of threads displayed on single page
MISAGO_THREADS_PER_PAGE = 25
MISAGO_THREADS_TAIL = 15


# Number of posts displayed on single thread page
MISAGO_POSTS_PER_PAGE = 15
MISAGO_POSTS_TAIL = 7


# Number of attachments possible to assign to single post
MISAGO_POST_ATTACHMENTS_LIMIT = 16

# Max allowed size of image before Misago will generate thumbnail for it
MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT = (500, 500)

# Length of secret used for attachments url tokens and filenames
MISAGO_ATTACHMENT_SECRET_LENGTH = 64

# Names of files served when user requests file that doesn't exist or is unavailable
# Those files will be sought within STATIC_ROOT directory
MISAGO_404_IMAGE = 'misago/img/error-404.png'
MISAGO_403_IMAGE = 'misago/img/error-403.png'


# Controls max age in days of items that Misago has to process to make rankings
# Used for active posters and most liked users lists
# If your forum runs out of memory when trying to generate users rankings list
# or you want those to be more dynamic, give this setting lower value
# You don't have to be overzelous with this as user rankings are cached for 24h
MISAGO_RANKING_LENGTH = 30

# Controls max number of items displayed on ranked lists
MISAGO_RANKING_SIZE = 50


# Controls number of users displayed on single page
MISAGO_USERS_PER_PAGE = 12


# Controls amount of data used by readtracking system
# Items older than number of days specified below are considered read
# Depending on amount of new content being posted on your forum you may want
# To decrease or increase this number to fine-tune readtracker performance
MISAGO_READTRACKER_CUTOFF = 40


# X-Sendfile
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


# Default forms templates
CRISPY_TEMPLATE_PACK = 'bootstrap3'


# Rest Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'misago.users.rest_permissions.IsAuthenticatedOrReadOnly',
    ),
    'EXCEPTION_HANDLER': 'misago.core.exceptionhandler.handle_api_exception',
    'UNAUTHENTICATED_USER': 'misago.users.models.AnonymousUser',
    'URL_FORMAT_OVERRIDE': None,
}


# Register Misago debug panels
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'misago.acl.panels.MisagoACLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
)
