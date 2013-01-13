from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.profiles.follows.views',
            url(r'^$', 'follows', name="user"),
            url(r'^$', 'follows', name="user_follows"),
        )
    else:
        urlpatterns += patterns('misago.profiles.follows.views',
            url(r'^follows/$', 'follows', name="user_follows"),
        )
    return urlpatterns