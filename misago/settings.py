"""Misago's default Django Project settings."""

__all__ = [
    "INSTALLED_APPS",
    "INSTALLED_PLUGINS",
    "MISAGO_ATTACHMENTS_SERVER",
    "MISAGO_DEFAULT_OG_IMAGE",
    "MISAGO_DEFAULT_OG_IMAGE_WIDTH",
    "MISAGO_DEFAULT_OG_IMAGE_HEIGHT",
    "MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES",
    "MISAGO_MIDDLEWARE",
    "MISAGO_NOTIFICATIONS_RETRY_DELAY",
    "MISAGO_PARSER_CLEAN_AST",
    "MISAGO_POST_ATTACHMENTS_LIMIT",
    "MISAGO_POST_LAST_LIKES_LIMIT",
    "MISAGO_POST_MENTIONS_LIMIT",
    "MISAGO_PYGMENTS_LANGUAGES",
    "MISAGO_PYGMENTS_STYLE",
    "MISAGO_QUOTED_POSTS_LIMIT",
    "TEMPLATE_CONTEXT_PROCESSORS",
]

INSTALLED_APPS = [
    # Misago overrides for Django core feature
    "misago",
    "misago.users",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps used by Misago
    "ariadne_django",
    "celery",
    "debug_toolbar",
    "mptt",
    "rest_framework",
    "social_django",
    # Misago apps
    "misago.account",
    "misago.acl",
    "misago.admin",
    "misago.analytics",
    "misago.apiv2",
    "misago.attachments",
    "misago.auth",
    "misago.cache",
    "misago.categories",
    "misago.components",
    "misago.conf",
    "misago.core",
    "misago.formats",
    "misago.forms",
    "misago.forumindex",
    "misago.graphql",
    "misago.html",
    "misago.htmx",
    "misago.icons",
    "misago.legal",
    "misago.likes",
    "misago.markup",
    "misago.menus",
    "misago.metatags",
    "misago.middleware",
    "misago.notifications",
    "misago.oauth2",
    "misago.pagination",
    "misago.parser",
    "misago.permissions",
    "misago.plugins",
    "misago.polls",
    "misago.postgres",
    "misago.posting",
    "misago.privatethreads",
    "misago.profile",
    "misago.readtracker",
    "misago.search",
    "misago.socialauth",
    "misago.themes",
    "misago.threads",
    "misago.edits",
    "misago.threadupdates",
]

INSTALLED_PLUGINS = []

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.i18n",
    "django.template.context_processors.media",
    "django.template.context_processors.request",
    "django.template.context_processors.static",
    "django.template.context_processors.tz",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "misago.context_processors.path.full_path",
    "misago.context_processors.categories.categories",
    "misago.context_processors.forumindex.main_menu",
    "misago.context_processors.htmx.is_request_htmx",
    "misago.context_processors.metatags.default_metatags",
    "misago.context_processors.permissions.user_permissions",
    "misago.context_processors.posting.syntax_highlighting",
    "misago.acl.context_processors.user_acl",
    "misago.conf.context_processors.conf",
    "misago.conf.context_processors.og_image",
    "misago.core.context_processors.misago_version",
    "misago.core.context_processors.request_path",
    "misago.core.context_processors.momentjs_locale",
    "misago.icons.context_processors.icons",
    "misago.search.context_processors.search_providers",
    "misago.themes.context_processors.theme",
    "misago.legal.context_processors.legal_links",
    "misago.menus.context_processors.menus",
    "misago.users.context_processors.user_links",
    "misago.core.context_processors.hooks",
    # Data preloaders
    "misago.conf.context_processors.preload_settings_json",
    "misago.core.context_processors.current_link",
    "misago.markup.context_processors.preload_api_url",
    "misago.users.context_processors.preload_user_json",
    "misago.socialauth.context_processors.preload_socialauth_json",
    # Note: keep frontend_context processor last for previous processors
    # to be able to expose data UI app via request.frontend_context
    "misago.core.context_processors.frontend_context",
]

MISAGO_MIDDLEWARE = [
    "misago.users.middleware.RealIPMiddleware",
    "misago.middleware.htmx.htmx_middleware",
    "misago.core.middleware.FrontendContextMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "misago.cache.middleware.cache_versions_middleware",
    "misago.conf.middleware.dynamic_settings_middleware",
    "misago.socialauth.middleware.socialauth_providers_middleware",
    "misago.users.middleware.UserMiddleware",
    "misago.middleware.permissions.permissions_middleware",
    "misago.middleware.categories.categories_middleware",
    "misago.acl.middleware.user_acl_middleware",
    "misago.core.middleware.ExceptionHandlerMiddleware",
    "misago.users.middleware.OnlineTrackerMiddleware",
    "misago.admin.middleware.AdminAuthMiddleware",
    "misago.middleware.privatethreads.sync_user_unread_private_threads",
]

MISAGO_ATTACHMENTS_SERVER = "misago.attachments.servers.django_redirect_response"

MISAGO_DEFAULT_OG_IMAGE = "misago/img/og-image.jpg"
MISAGO_DEFAULT_OG_IMAGE_WIDTH = 1200
MISAGO_DEFAULT_OG_IMAGE_HEIGHT = 630

MISAGO_EMAIL_CHANGE_TOKEN_EXPIRES = 48  # Hours

MISAGO_NOTIFICATIONS_RETRY_DELAY = 5  # Seconds

MISAGO_POST_ATTACHMENTS_LIMIT = 64

MISAGO_POST_LAST_LIKES_LIMIT = 25

MISAGO_POST_MENTIONS_LIMIT = 50
MISAGO_QUOTED_POSTS_LIMIT = 20

# Choices: https://pygments.org/styles/
MISAGO_PYGMENTS_STYLE = "default"

# Choices: https://pygments.org/languages/
MISAGO_PYGMENTS_LANGUAGES = (
    "apacheconf",
    "bash",
    "c",
    "csharp",
    "cpp",
    "css",
    "cuda",
    "d",
    "dart",
    "docker",
    "elm",
    "erlang",
    "fsharp",
    "gdscript",
    "glsl",
    "go",
    "graphql",
    "handlebars",
    "haskell",
    "html",
    "http",
    "java",
    "jsp",
    "javascript",
    "json",
    "jsx",
    "julia",
    "kotlin",
    "less",
    "lua",
    "mako",
    "markdown",
    "matlab",
    "numpy",
    "objective-c",
    "ocaml",
    "octave",
    "pawn",
    "perl",
    "perl6",
    "php",
    "prolog",
    "python",
    "python2",
    "racket",
    "restructuredtext",
    "ruby",
    "rust",
    "sass",
    "scala",
    "scilab",
    "scss",
    "smalltalk",
    "smarty",
    "sql",
    "swift",
    "txt",
    "toml",
    "twig",
    "typescript",
    "vue",
    "wikitext",
    "xml",
    "yaml",
    "zig",
)

# For use in tests only
MISAGO_PARSER_CLEAN_AST = True
