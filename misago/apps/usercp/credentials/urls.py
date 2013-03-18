from django.conf.urls import patterns, url

def register_usercp_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.usercp.credentials.views',
            url(r'^$', 'credentials', name="usercp"),
            url(r'^$', 'credentials', name="usercp_credentials"),
        )
    else:
        urlpatterns += patterns('misago.apps.usercp.credentials.views',
            url(r'^credentials/$', 'credentials', name="usercp_credentials"),
        )

    urlpatterns += patterns('misago.apps.usercp.credentials.views',
        url(r'^credentials/activate/(?P<token>[a-zA-Z0-9]+)/$', 'activate', name="usercp_credentials_activate"),
    )
    
    return urlpatterns
