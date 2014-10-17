from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.readtracker.views',
    url(r'^read-all/$', 'read_all', name='read_all'),
    url(r'^read-forum/(?P<forum_id>\d+)/$', 'read_forum', name='read_forum'),
)
