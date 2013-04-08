from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.reports.views',
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/$', 'ThreadsListView', name="reports"),
    url(r'^forum/(?P<slug>(\w|-)+)-(?P<forum>\d+)/(?P<page>[^0]\d+)/$', 'ThreadsView', name="reports"),
)
