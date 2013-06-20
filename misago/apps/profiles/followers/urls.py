from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.followers.views',
            url(r'^$', 'followers', name="user"),
            url(r'^$', 'followers', name="user_followers"),
            url(r'^(?P<page>[1-9]([0-9]+)?)/$', 'followers', name="user_followers"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.followers.views',
            url(r'^followers/$', 'followers', name="user_followers"),
            url(r'^followers/(?P<page>[1-9]([0-9]+)?)/$', 'followers', name="user_followers"),
        )
    return urlpatterns