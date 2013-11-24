from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.search.views',
    url(r'^$', 'SearchForumsView', name="search_forums"),
    url(r'^quick/$', 'QuickSearchView', name="search_quick"),
    url(r'^private-threads/$', 'SearchPrivateThreadsView', name="search_private_threads"),
    url(r'^reports/$', 'SearchReportsView', name="search_reports"),
    url(r'^results/$', 'SearchResultsView', name="search_results"),
    url(r'^results/(?P<page>[1-9]([0-9]+)?)/$', 'SearchResultsView', name="search_results"),
)
