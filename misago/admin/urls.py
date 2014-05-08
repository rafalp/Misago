from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_by_path


urlpatterns = patterns('misago.admin.views',
    # "misago:admin:index" link symbolises "root" of Misago admin links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago Admin and will be checked by Misago Admin Middleware
    url(r'^$', 'index.admin_index', name='index'),
    url(r'^logout/$', 'auth.logout', name='logout'),
)


def discover_admin_urls():
    SEARCH_PATTERNS = (
        '%s.urls.adminurlpatterns',
        '%s.urls.admin.urlpatterns',
        '%s.adminurls.urlpatterns',
        )
    admin_patterns = []

    for app in settings.INSTALLED_APPS:
        for pattern in SEARCH_PATTERNS:
            try:
                admin_patterns += import_by_path(pattern % app)
                continue
            except ImproperlyConfigured:
                pass

    return admin_patterns


"""
TEST PATTERNS FOR GOD OF TEST PATTERNS
"""

userpatterns = patterns('misago.admin.views',
    # top lel at users fake views
    url(r'^$', 'index.admin_index', name='list'),
)


newpatterns = patterns('',
    url(r'^', include(userpatterns, namespace='accounts')),
)


urlpatterns += patterns('',
    url(r'^users/', include(newpatterns, namespace='users')),
)
