from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.credentials.views',
    url(r'^credentials/$', 'credentials', name="usercp_credentials"),
)