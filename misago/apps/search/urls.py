from django.conf.urls import patterns, url

urlpatterns = patterns('misago.apps.search.views',
    url(r'^$', 'do_search', name="search"),
    url(r'^results/$', 'show_sesults', name="search_results"),
)