from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.details.views',
            url(r'^$', 'details', name="user"),
            url(r'^$', 'details', name="user_details"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.details.views',
            url(r'^details/$', 'details', name="user_details"),
        )
    return urlpatterns