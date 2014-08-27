from django.conf.urls import patterns, include, url

from misago.threads.views.threads import (ForumView, ThreadView, StartThreadView,
                                          ReplyView, EditView)


urlpatterns = patterns('',
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/show-(?P<show>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/sort-(?P<sort>[\w-]+)/show-(?P<show>[\w-]+)/(?P<page>\d+)/$', ForumView.as_view(), name='forum'),
    url(r'^forum/(?P<forum_slug>[\w\d-]+)-(?P<forum_id>\d+)/start-thread/$', StartThreadView.as_view(), name='start_thread'),
)

urlpatterns += patterns('',
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/$', ThreadView.as_view(), name='thread'),
    url(r'^thread/(?P<thread_slug>[\w\d-]+)-(?P<thread_id>\d+)/(?P<page>\d+)/$', ThreadView.as_view(), name='thread'),
)
