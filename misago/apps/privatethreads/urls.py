from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.privatethreads.views',
    url(r'^$', 'ThreadsListView', name="private_threads"),
    url(r'^(?P<page>\d+)/$', 'ThreadsView', name="private_threads"),
)
