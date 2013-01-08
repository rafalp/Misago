from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.username.views',
    url(r'^username/$', 'username', name="usercp_username"),
)
