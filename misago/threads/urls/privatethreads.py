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


# thread view
from misago.threads.views.privatethreads import ThreadView
urlpatterns += patterns('',
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/$', ThreadView.as_view(), name='private_thread'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/(?P<page>\d+)/$', ThreadView.as_view(), name='private_thread'),
)


# goto views
from misago.threads.views.privatethreads import (GotoLastView, GotoNewView,
                                                 GotoPostView)
urlpatterns += patterns('',
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/last/$', GotoLastView.as_view(), name='private_thread_last'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/new/$', GotoNewView.as_view(), name='private_thread_new'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/post-(?P<post_id>\d+)/$', GotoPostView.as_view(), name='private_thread_post'),
)


# reported posts views
from misago.threads.views.privatethreads import ReportedPostsListView
urlpatterns += patterns('',
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/reported-posts/$', ReportedPostsListView.as_view(), name='private_thread_reported'),
)


# participants views
from misago.threads.views.privatethreads import (ThreadParticipantsView,
                                                 EditThreadParticipantsView,
                                                 AddThreadParticipantsView,
                                                 RemoveThreadParticipantView,
                                                 LeaveThreadView)
urlpatterns += patterns('',
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/participants/$', ThreadParticipantsView.as_view(), name='private_thread_participants'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/edit-participants/$', EditThreadParticipantsView.as_view(), name='private_thread_edit_participants'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/remove-participant/(?P<user_id>\d+)/$', RemoveThreadParticipantView.as_view(), name='private_thread_remove_participant'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/add-participants/$', AddThreadParticipantsView.as_view(), name='private_thread_add_participants'),
    url(r'^private-thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/leave/$', LeaveThreadView.as_view(), name='private_thread_leave'),
)


# post views
from misago.threads.views.privatethreads import (QuotePostView, HidePostView,
                                                 UnhidePostView,
                                                 DeletePostView,
                                                 ReportPostView)
urlpatterns += patterns('',
    url(r'^private-post/(?P<post_id>\d+)/quote/$', QuotePostView.as_view(), name='quote_private_post'),
    url(r'^private-post/(?P<post_id>\d+)/unhide/$', UnhidePostView.as_view(), name='unhide_private_post'),
    url(r'^private-post/(?P<post_id>\d+)/hide/$', HidePostView.as_view(), name='hide_private_post'),
    url(r'^private-post/(?P<post_id>\d+)/delete/$', DeletePostView.as_view(), name='delete_private_post'),
    url(r'^private-post/(?P<post_id>\d+)/report/$', ReportPostView.as_view(), name='report_private_post'),
)


# events view
from misago.threads.views.privatethreads import EventsView
urlpatterns += patterns('',
    url(r'^edit-private-event/(?P<event_id>\d+)/$', EventsView.as_view(), name='edit_private_event'),
)


# posting views
from misago.threads.views.privatethreads import PostingView
urlpatterns += patterns('',
    url(r'^start-private-thread/$', PostingView.as_view(), name='start_private_thread'),
    url(r'^reply-private-thread/(?P<thread_id>\d+)/$', PostingView.as_view(), name='reply_private_thread'),
    url(r'^edit-private_post/(?P<thread_id>\d+)/(?P<post_id>\d+)/edit/$', PostingView.as_view(), name='edit_private_post'),
)
