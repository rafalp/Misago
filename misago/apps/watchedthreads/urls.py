from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.watchedthreads.views',
    url(r'^/$', 'watched_threads', name="watched_threads"),
    url(r'^(?P<page>\d+)/$', 'watched_threads', name="watched_threads"),
    url(r'^new/$', 'watched_threads', name="watched_threads_new", kwargs={'new': True}),
    url(r'^new/(?P<page>\d+)/$', 'watched_threads', name="watched_threads_new", kwargs={'new': True}),
)
