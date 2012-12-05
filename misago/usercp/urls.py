from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.views',
    url(r'^$', 'options', name="usercp"),
    url(r'^credentials/$', 'credentials', name="usercp_credentials"),
    url(r'^username/$', 'username', name="usercp_username"),
    url(r'^avatar/$', 'avatar', name="usercp_avatar"),
    url(r'^signature/$', 'signature', name="usercp_signature"),
    url(r'^ignored/$', 'ignored', name="usercp_ignored"),
)