from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.announcements.views',
    url(r'^$', 'ThreadsListView', name="announcements"),
    url(r'^(?P<page>\d+)/$', 'ThreadsListView', name="announcements"),
)
