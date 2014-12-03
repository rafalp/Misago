from django.conf.urls import patterns, include, url


from misago.threads.views.privatethreads import ThreadsView
urlpatterns = patterns('',
    url(r'^private-threads/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/(?P<page>\d+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/(?P<page>\d+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/show-(?P<show>[\w-]+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/$', ThreadsView.as_view(), name='private_threads'),
    url(r'^private-threads/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ThreadsView.as_view(), name='private_threads'),
)


from misago.threads.views.privatethreads import (ThreadView, GotoLastView,
                                                 GotoNewView, GotoPostView)
urlpatterns += patterns('',
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/$', ThreadView.as_view(), name='private_thread'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/(?P<page>\d+)/$', ThreadView.as_view(), name='private_thread'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/last/$', GotoLastView.as_view(), name='private_thread_last'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/new/$', GotoNewView.as_view(), name='private_thread_new'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/post-(?P<post_id>\d+)/$', GotoPostView.as_view(), name='private_thread_post'),
)


from misago.threads.views.privatethreads import PostingView
urlpatterns += patterns('',
    url(r'^start-private-thread/$', PostingView.as_view(), name='start_private_thread'),
    url(r'^reply-private-thread/(?P<thread_id>\d+)/$', PostingView.as_view(), name='reply_private_thread'),
)
