from django.conf.urls import patterns, url

urlpatterns = patterns('misago.watcher.views',
    url(r'^watched/$', 'watched_threads', name="watched_threads"),
    url(r'^watched/(?P<page>\d+)/$', 'watched_threads', name="watched_threads"),
    url(r'^watched/new/$', 'watched_threads', name="watched_threads_new", kwargs={'new': True}),
    url(r'^watched/new/(?P<page>\d+)/$', 'watched_threads', name="watched_threads_new", kwargs={'new': True}),
)
