from django.conf.urls import patterns, include, url


urlpatterns = patterns('misago.forums.views',
    url(r'^category/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/$', 'category', name='category'),
    url(r'^redirect/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/$', 'redirect', name='redirect'),
)
