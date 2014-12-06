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
            'misago/js/jquery.mousewheel.js',
            'misago/js/bootstrap.js',
            'misago/js/moment.min.js',
            'misago/js/tinycon.min.js',
            'misago/js/typeahead.jquery.min.js',
            'misago/js/misago.js',
            'misago/js/misago-storage.js',
            'misago/js/misago-alerts.js',
            'misago/js/misago-ajax.js',
            'misago/js/misago-dom.js',
            'misago/js/misago-timestamps.js',
            'misago/js/misago-uiserver.js',
            'misago/js/misago-bindings.js',
            'misago/js/misago-tooltips.js',
            'misago/js/misago-datetimepicker.js',
            'misago/js/misago-yesnoswitch.js',
            'misago/js/misago-dropdowns.js',
            'misago/js/misago-modal.js',
            'misago/js/misago-scrolling.js',
            'misago/js/misago-notifications.js',
            'misago/js/misago-threads-lists.js',
            'misago/js/misago-onebox.js',
            'misago/js/misago-posting.js',
            'misago/js/misago-posting-participants.js',
            'misago/js/misago-posts.js',
        ),
        'output_filename': 'misago.js',
    },
    'misago_editor': {
        'source_filenames': (
            'misago/js/jquery.autosize.js',
            'misago/js/misago-editor.js',
        ),
        'output_filename': 'misago-editor.js',
    },
    'misago_admin': {
        'source_filenames': (
            'misago/admin/js/jquery.js',
            'misago/admin/js/bootstrap.js',
            'misago/admin/js/moment.min.js',
            'misago/admin/js/bootstrap-datetimepicker.min.js',
            'misago/admin/js/misago-datetimepicker.js',
            'misago/admin/js/misago-timestamps.js',
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
    'pipeline',
    'crispy_forms',
    'mptt',
    'misago.admin',
    'misago.acl',
    'misago.core',
    'misago.conf',
    'misago.markup',
    'misago.notifications',
    'misago.legal',
    'misago.forums',
    'misago.threads',
    'misago.readtracker',
    'misago.faker',
)

MIDDLEWARE_CLASSES = (
    'misago.users.middleware.AvatarServerMiddleware',
    'misago.users.middleware.RealIPMiddleware',
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
    'misago.users.context_processors.sites_links',
)

MISAGO_ACL_EXTENSIONS = (
    'misago.users.permissions.account',
    'misago.users.permissions.profiles',
    'misago.users.permissions.warnings',
    'misago.users.permissions.moderation',
    'misago.users.permissions.delete',
    'misago.forums.permissions',
    'misago.threads.permissions.threads',
    'misago.threads.permissions.privatethreads',
)

MISAGO_MARKUP_EXTENSIONS = ()

MISAGO_POSTING_MIDDLEWARES = (
    # Note: always keep FloodProtectionMiddleware middleware first one
    'misago.threads.posting.floodprotection.FloodProtectionMiddleware',
    'misago.threads.posting.reply.ReplyFormMiddleware',
    'misago.threads.posting.participants.ThreadParticipantsFormMiddleware',
    'misago.threads.posting.threadlabel.ThreadLabelFormMiddleware',
    'misago.threads.posting.threadpin.ThreadPinFormMiddleware',
    'misago.threads.posting.threadclose.ThreadCloseFormMiddleware',
    'misago.threads.posting.recordedit.RecordEditMiddleware',
    'misago.threads.posting.updatestats.UpdateStatsMiddleware',
    # Note: always keep SaveChangesMiddleware middleware last one
    'misago.threads.posting.savechanges.SaveChangesMiddleware',
)

MISAGO_THREAD_TYPES = (
    # category and redirect types
    'misago.forums.forumtypes.RootCategory',
    'misago.forums.forumtypes.Category',
    'misago.forums.forumtypes.Redirect',
    # real thread types
    'misago.threads.threadtypes.forumthread.ForumThread',
    'misago.threads.threadtypes.privatethread.PrivateThread',
    'misago.threads.threadtypes.report.Report',
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

# For which sizes avatars should be cached?
# Keep sizes ordered from greatest to smallest
MISAGO_AVATARS_SIZES = (400, 200, 150, 100, 64, 50, 30, 20)

# Path to avatar server
# This path is used to detect avatar requests, which bypass most of
# Request/Response processing for performance reasons
MISAGO_AVATAR_SERVER_PATH = '/user-avatar'


# Controls max age in days of items that Misago has to process to make rankings
# Used for active posters and most liked users lists
# If your forum runs out of memory when trying to generate users rankings list
# or you want those to be more dynamic, give this setting lower value
# You don't have to be overzelous with this as user rankings are cached for 24h
MISAGO_RANKING_LENGTH = 30

# Controls max number of items displayed on ranked lists
MISAGO_RANKING_SIZE = 30


# Controls amount of data used for new threads/replies lists
# Only unread threads younger than number of days specified in this setting
# will be considered fresh for "new threads" list
# Only unread threads with last reply younger than number of days specified
# there will be confidered fresh for "Threads with unread replies" list
MISAGO_FRESH_CONTENT_PERIOD = 40

# Number of minutes between updates of new content counts like new threads,
# unread replies or moderated threads/posts
MISAGO_CONTENT_COUNTING_FREQUENCY = 5


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
