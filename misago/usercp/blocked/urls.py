from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.blocked.views',
    url(r'^blocked/$', 'blocked', name="usercp_blocked"),
)
