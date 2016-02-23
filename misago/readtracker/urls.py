from django.conf.urls import include, patterns, url


urlpatterns = patterns('misago.readtracker.views',
    url(r'^read-all/$', 'read_all', name='read_all'),
    url(r'^read-category/(?P<category_id>\d+)/$', 'read_category', name='read_category'),
)
