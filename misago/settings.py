"""Misago's default Django Project settings"""

__all__ = [
    "INSTALLED_APPS",
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
    "misago.admin",
    "misago.acl",
    "misago.analytics",
    "misago.cache",
    "misago.core",
    "misago.conf",
    "misago.icons",
    "misago.themes",
    "misago.markup",
    "misago.legal",
    "misago.notifications",
    "misago.categories",
    "misago.threads",
    "misago.readtracker",
    "misago.search",
    "misago.oauth2",
    "misago.socialauth",
    "misago.graphql",
    "misago.faker",
    "misago.menus",
    "misago.plugins",
    "misago.apiv2",
]