from django.conf import settings
from django.conf.urls import patterns, url


if settings.MISAGO_CATEGORIES_ON_INDEX:
    URL_PATH = r'^threads/$'
else:
    URL_PATH = r'^$'


urlpatterns = patterns('misago.threads.views.threadslist',
    url(URL_PATH, 'threads_list', name='threads'),

    url(r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/$', 'threads_list', name='category'),
)