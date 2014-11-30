from django.conf.urls import patterns, include, url


from misago.threads.views.privatethreads import PrivateThreadsView
urlpatterns = patterns('',
    url(r'^private-threads/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/(?P<page>\d+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/(?P<page>\d+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/show-(?P<show>[\w-]+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/$', PrivateThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', PrivateThreadsView.as_view(), name='private_threads'),
)
