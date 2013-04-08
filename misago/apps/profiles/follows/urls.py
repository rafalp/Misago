from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.follows.views',
            url(r'^$', 'follows', name="user"),
            url(r'^$', 'follows', name="user_follows"),
            url(r'^(?P<page>[^0]\d+)/$', 'follows', name="user_follows"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.follows.views',
            url(r'^follows/$', 'follows', name="user_follows"),
            url(r'^follows/(?P<page>[^0]\d+)/$', 'follows', name="user_follows"),
        )
    return urlpatterns