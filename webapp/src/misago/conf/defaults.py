# pylint: disable=line-too-long
"""
Default Misago settings. Override these with settings in the module pointed to
by the DJANGO_SETTINGS_MODULE environment variable.

If you rely on any of those in your code, make sure you use `misago.conf.settings`
instead of Django's `django.conf.settings`.
"""

# Permissions system extensions
# https://misago.readthedocs.io/en/latest/developers/acls.html#extending-permissions-system

MISAGO_ACL_EXTENSIONS = [
    "misago.users.permissions.account",
    "misago.users.permissions.profiles",
    "misago.users.permissions.moderation",
    "misago.users.permissions.delete",
    "misago.categories.permissions",
    "misago.threads.permissions.attachments",
    "misago.threads.permissions.polls",
    "misago.threads.permissions.threads",
    "misago.threads.permissions.privatethreads",
    "misago.threads.permissions.bestanswers",
    "misago.search.permissions",
]


# Path to the directory that Misago should use to prepare user data downloads.
# Should not be accessible from internet.

MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR = None


# Custom markup extensions

MISAGO_MARKUP_EXTENSIONS = []


# Bleach callbacks for linkifying paragraphs

MISAGO_BLEACH_CALLBACKS = []


# Custom post validators

MISAGO_POST_VALIDATORS = []


# Post search filters

MISAGO_POST_SEARCH_FILTERS = []


# Posting middlewares
# https://misago.readthedocs.io/en/latest/developers/posting_process.html

MISAGO_POSTING_MIDDLEWARES = [
    # Always keep FloodProtectionMiddleware middleware first one
    "misago.threads.api.postingendpoint.floodprotection.FloodProtectionMiddleware",
    "misago.threads.api.postingendpoint.category.CategoryMiddleware",
    "misago.threads.api.postingendpoint.privatethread.PrivateThreadMiddleware",
    "misago.threads.api.postingendpoint.reply.ReplyMiddleware",
    "misago.threads.api.postingendpoint.moderationqueue.ModerationQueueMiddleware",
    "misago.threads.api.postingendpoint.attachments.AttachmentsMiddleware",
    "misago.threads.api.postingendpoint.participants.ParticipantsMiddleware",
    "misago.threads.api.postingendpoint.pin.PinMiddleware",
    "misago.threads.api.postingendpoint.close.CloseMiddleware",
    "misago.threads.api.postingendpoint.hide.HideMiddleware",
    "misago.threads.api.postingendpoint.protect.ProtectMiddleware",
    "misago.threads.api.postingendpoint.recordedit.RecordEditMiddleware",
    "misago.threads.api.postingendpoint.updatestats.UpdateStatsMiddleware",
    "misago.threads.api.postingendpoint.mentions.MentionsMiddleware",
    "misago.threads.api.postingendpoint.subscribe.SubscribeMiddleware",
    "misago.threads.api.postingendpoint.syncprivatethreads.SyncPrivateThreadsMiddleware",
    # Always keep SaveChangesMiddleware middleware after all state-changing middlewares
    "misago.threads.api.postingendpoint.savechanges.SaveChangesMiddleware",
    # Those middlewares are last because they don't change app state
    "misago.threads.api.postingendpoint.emailnotification.EmailNotificationMiddleware",
]


# Configured thread types

MISAGO_THREAD_TYPES = [
    "misago.threads.threadtypes.thread.Thread",
    "misago.threads.threadtypes.privatethread.PrivateThread",
]


# Search extensions

MISAGO_SEARCH_EXTENSIONS = [
    "misago.threads.search.SearchThreads",
    "misago.users.search.SearchUsers",
]


# Additional registration validators
# https://misago.readthedocs.io/en/latest/developers/validating_registrations.html

MISAGO_NEW_REGISTRATIONS_VALIDATORS = [
    "misago.users.validators.validate_gmail_email",
    "misago.users.validators.validate_with_sfs",
]


# Custom profile fields

MISAGO_PROFILE_FIELDS = []


# Login API URL

MISAGO_LOGIN_API_URL = "auth"


# Misago Admin Path
# Omit starting and trailing slashes. To disable Misago admin, empty this value.

MISAGO_ADMIN_PATH = "admincp"


# Admin urls namespaces that Misago's AdminAuthMiddleware should protect

MISAGO_ADMIN_NAMESPACES = ["admin", "misago:admin"]


# How long (in minutes) since previous request to admin namespace should admin session last.

MISAGO_ADMIN_SESSION_EXPIRATION = 60


# Display threads on forum index
# Change this to false to display categories list instead

MISAGO_THREADS_ON_INDEX = True


# Function used for generating individual avatar for user

MISAGO_DYNAMIC_AVATAR_DRAWER = "misago.users.avatars.dynamic.draw_default"


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command

MISAGO_AVATAR_GALLERY = None


# Save user avatars for sizes
# Keep sizes ordered from greatest to smallest
# Max size also controls min size of uploaded image as well as crop size

MISAGO_AVATARS_SIZES = [400, 200, 150, 100, 64, 50, 30]


# Path to blank avatar image used for guests and removed users.

MISAGO_BLANK_AVATAR = "misago/img/blank-avatar.png"


# Max allowed size of image before Misago will generate thumbnail for it

MISAGO_ATTACHMENT_IMAGE_SIZE_LIMIT = (500, 500)


# Length of secret used for attachments url tokens and filenames

MISAGO_ATTACHMENT_SECRET_LENGTH = 64


# Names of files served when user requests file that doesn't exist or is unavailable

MISAGO_ATTACHMENT_403_IMAGE = "misago/img/attachment-403.png"
MISAGO_ATTACHMENT_404_IMAGE = "misago/img/attachment-404.png"


# Available Moment.js locales

MISAGO_MOMENT_JS_LOCALES = [
    "af",
    "ar-ma",
    "ar-sa",
    "ar-tn",
    "ar",
    "az",
    "be",
    "bg",
    "bn",
    "bo",
    "br",
    "bs",
    "ca",
    "cs",
    "cv",
    "cy",
    "da",
    "de-at",
    "de",
    "el",
    "en-au",
    "en-ca",
    "en-gb",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fi",
    "fo",
    "fr-ca",
    "fr",
    "fy",
    "gl",
    "he",
    "hi",
    "hr",
    "hu",
    "hy-am",
    "id",
    "is",
    "it",
    "ja",
    "ka",
    "km",
    "ko",
    "lb",
    "lt",
    "lv",
    "mk",
    "ml",
    "mr",
    "ms-my",
    "my",
    "nb",
    "ne",
    "nl",
    "nn",
    "pl",
    "pt-br",
    "pt",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr-cyrl",
    "sr",
    "sv",
    "ta",
    "th",
    "tl-ph",
    "tr",
    "tzm-latn",
    "tzm",
    "uk",
    "uz",
    "vi",
    "zh-cn",
    "zh-hans",
    "zh-tw",
]
