from django.conf.urls import patterns, include, url


# category view
from misago.threads.views.threads import CategoryView
urlpatterns = patterns('',
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/(?P<page>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/sort-(?P<sort>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/sort-(?P<sort>[\w-]+)/(?P<page>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/show-(?P<show>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^category/(?P<category_slug>[\w\d-]+)-(?P<category_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', CategoryView.as_view(), name='category'),
)


# thread view
from misago.threads.views.threads import ThreadView
urlpatterns += patterns('',
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/$', ThreadView.as_view(), name='thread'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/(?P<page>\d+)/$', ThreadView.as_view(), name='thread'),
)


# goto views
from misago.threads.views.threads import (GotoLastView, GotoNewView,
                                          GotoPostView)
urlpatterns += patterns('',
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/last/$', GotoLastView.as_view(), name='thread_last'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/new/$', GotoNewView.as_view(), name='thread_new'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/post-(?P<post_id>\d+)/$', GotoPostView.as_view(), name='thread_post'),
)


# moderated/reported posts views
from misago.threads.views.threads import (ModeratedPostsListView,
                                          ReportedPostsListView)
urlpatterns += patterns('',
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/moderation-queue/$', ModeratedPostsListView.as_view(), name='thread_moderated'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/reported-posts/$', ReportedPostsListView.as_view(), name='thread_reported'),
)


# post views
from misago.threads.views.threads import (QuotePostView, ApprovePostView,
                                          HidePostView, UnhidePostView,
                                          DeletePostView, ReportPostView)
urlpatterns += patterns('',
    url(r'^post/(?P<post_id>\d+)/quote/$', QuotePostView.as_view(), name='quote_post'),
    url(r'^post/(?P<post_id>\d+)/approve/$', ApprovePostView.as_view(), name='approve_post'),
    url(r'^post/(?P<post_id>\d+)/unhide/$', UnhidePostView.as_view(), name='unhide_post'),
    url(r'^post/(?P<post_id>\d+)/hide/$', HidePostView.as_view(), name='hide_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', DeletePostView.as_view(), name='delete_post'),
    url(r'^post/(?P<post_id>\d+)/report/$', ReportPostView.as_view(), name='report_post'),
)


# events view
from misago.threads.views.threads import EventsView
urlpatterns += patterns('',
    url(r'^edit-event/(?P<event_id>\d+)/$', EventsView.as_view(), name='edit_event'),
)


# posting views
from misago.threads.views.threads import PostingView
urlpatterns += patterns('',
    url(r'^start-thread/(?P<category_id>\d+)/$', PostingView.as_view(), name='start_thread'),
    url(r'^reply-thread/(?P<category_id>\d+)/(?P<thread_id>\d+)/$', PostingView.as_view(), name='reply_thread'),
    url(r'^edit-post/(?P<category_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/edit/$', PostingView.as_view(), name='edit_post'),
)


# new threads list
from misago.threads.views.newthreads import NewThreadsView, clear_new_threads
urlpatterns += patterns('',
    url(r'^new-threads/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/(?P<page>\d+)/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/sort-(?P<sort>[\w-]+)$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/sort-(?P<sort>[\w-]+)(?P<page>\d+)/$', NewThreadsView.as_view(), name='new_threads'),
    url(r'^new-threads/clear/$', clear_new_threads, name='clear_new_threads'),
)


# unread threads list
from misago.threads.views.unreadthreads import (UnreadThreadsView,
                                                clear_unread_threads)
urlpatterns += patterns('',
    url(r'^unread-threads/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/(?P<page>\d+)/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/sort-(?P<sort>[\w-]+)$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/sort-(?P<sort>[\w-]+)(?P<page>\d+)/$', UnreadThreadsView.as_view(), name='unread_threads'),
    url(r'^unread-threads/clear/$', clear_unread_threads, name='clear_unread_threads'),
)


# moderated content list
from misago.threads.views.moderatedcontent import ModeratedContentView
urlpatterns += patterns('',
    url(r'^moderated-content/$', ModeratedContentView.as_view(), name='moderated_content'),
    url(r'^moderated-content/(?P<page>\d+)/$', ModeratedContentView.as_view(), name='moderated_content'),
    url(r'^moderated-content/sort-(?P<sort>[\w-]+)$', ModeratedContentView.as_view(), name='moderated_content'),
    url(r'^moderated-content/sort-(?P<sort>[\w-]+)(?P<page>\d+)/$', ModeratedContentView.as_view(), name='moderated_content'),
)
