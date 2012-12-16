from django.conf.urls import patterns, url

urlpatterns = patterns('misago.usercp.credentials.views',
    url(r'^credentials/$', 'credentials', name="usercp_credentials"),
    url(r'^credentials/activate/(?P<token>[a-zA-Z0-9]+)/$', 'activate', name="usercp_credentials_activate"),
)