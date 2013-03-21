from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.announcements',
    url(r'^$', 'list.ThreadsListView', name="announcements"),
    url(r'^(?P<page>\d+)/$', 'list.ThreadsListView', name="announcements"),
    url(r'^new/$', 'posting.NewThreadView', name="announcement_start"),
)
