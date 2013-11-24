from django.conf.urls import patterns, url

def register_profile_urls(first=False):
    urlpatterns = []
    if first:
        urlpatterns += patterns('misago.apps.profiles.posts.views',
            url(r'^$', 'posts', name="user"),
            url(r'^$', 'posts', name="user_posts"),
            url(r'^(?P<page>[1-9]([0-9]+)?)/$', 'posts', name="user_posts"),
        )
    else:
        urlpatterns += patterns('misago.apps.profiles.posts.views',
            url(r'^posts/$', 'posts', name="user_posts"),
            url(r'^posts/(?P<page>[1-9]([0-9]+)?)/$', 'posts', name="user_posts"),
        )
    return urlpatterns