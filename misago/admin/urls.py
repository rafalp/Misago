import importlib
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.exceptions import ImproperlyConfigured
from misago import admin


urlpatterns = patterns('misago.admin.views',
    # "misago:admin:index" link symbolises "root" of Misago admin links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago Admin and will be checked by Misago Admin Middleware
    url(r'^$', 'index.admin_index', name='index'),
    url(r'^logout/$', 'auth.logout', name='logout'),
)


# Import admin urls
import misago.conf.adminurls
import misago.acl.adminurls
import misago.users.urls.admin

# Register discovered patterns
urlpatterns += admin.urlpatterns()
