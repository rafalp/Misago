from django.conf.urls import patterns, include, url
from misago import admin


urlpatterns = patterns('misago.admin.views',
    # "misago:admin:index" link symbolises "root" of Misago admin links space
    # any request with path that falls below this one is assumed to be directed
    # at Misago Admin and will be checked by Misago Admin Middleware
    url(r'^$', 'index.admin_index', name='index'),
    url(r'^resolve-version/$', 'index.check_version', name='check_version'),
    url(r'^logout/$', 'auth.logout', name='logout'),
)


# Discover admin and register patterns
admin.discover_misago_admin()
urlpatterns += admin.urlpatterns()
