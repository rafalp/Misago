from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.profiles.content.views',
            url(r'^$', 'posts', name="user"),
            url(r'^$', 'posts', name="user_posts"),
            url(r'^(?P<page>\d+)/$', 'posts', name="user_posts"),
            url(r'^threads/$', 'threads', name="user_threads"),
        )
    else:
        urlpatterns += patterns('misago.profiles.content.views',
            url(r'^posts/$', 'posts', name="user_posts"),
            url(r'^posts/(?P<page>\d+)/$', 'posts', name="user_posts"),
            url(r'^threads/$', 'threads', name="user_threads"),
        )
    urlpatterns += patterns('misago.profiles.content.views',
        url(r'^threads/(?P<page>\d+)/$', 'threads', name="user_threads"),
    )
    return urlpatterns