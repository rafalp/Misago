import importlib
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.exceptions import ImproperlyConfigured
from misago.admin import site


urlpatterns = patterns('misago.admin.views',
    # "misago:admin:index" link symbolises "root" of Misago admin links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago Admin and will be checked by Misago Admin Middleware
    url(r'^$', 'index.admin_index', name='index'),
    url(r'^logout/$', 'auth.logout', name='logout'),
)


# Magic voodoo for initializing admin patterns lazily
def initialize_admin_urls():
    SEARCH_PATTERNS = (
        '%s.adminurls',
        '%s.urls.admin',
        )

    for app in settings.INSTALLED_APPS:
        for pattern in SEARCH_PATTERNS:
            try:
                importlib.import_module(pattern % app)
                continue
            except ImportError:
                pass


# Register discovered patterns
initialize_admin_urls()
urlpatterns += site.urlpatterns()
