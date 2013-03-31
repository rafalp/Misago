from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.threads.views',
            url(r'^$', 'threads', name="user"),
            url(r'^$', 'threads', name="user_threads"),
            url(r'^(?P<page>\d+)/$', 'threads', name="user_threads"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.threads.views',
            url(r'^threads/$', 'threads', name="user_threads"),
            url(r'^threads/(?P<page>\d+)/$', 'threads', name="user_threads"),
        )
    return urlpatterns