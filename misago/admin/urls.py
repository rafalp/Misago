from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('misago.admin.views',
    # "misago:admin:index" link symbolises "root" of Misago admin links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago Admin and will be checked by Misago Admin Middleware
    url(r'^$', 'index.admin_index', name='index'),
    url(r'^settings/$', 'index.admin_index', name='settings'),
)


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
