from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.search.views',
    url(r'^$', 'QuickSearchView', name="search"),
    url(r'^results/$', 'SearchResultsView', name="search_results"),
    url(r'^results/(?P<page>[1-9]([0-9]+)?)/$', 'SearchResultsView', name="search_results"),
)
