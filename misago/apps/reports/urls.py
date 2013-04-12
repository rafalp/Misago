from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.reports.views',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'ThreadsListView', name="reports"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>[1-9]([0-9]+)?)/$', 'ThreadsView', name="reports"),
)
