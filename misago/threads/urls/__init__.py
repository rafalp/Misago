from django.conf import settings
from django.conf.urls import url

from ..views.attachment import attachment_server
from ..views.goto import ThreadGotoPostView, ThreadGotoLastView, ThreadGotoNewView, ThreadGotoUnapprovedView
from ..views.list import ForumThreads, CategoryThreads, PrivateThreads
from ..views.thread import Thread, PrivateThread


LISTS_TYPES = (
    'all',
    'my',
    'new',
    'unread',
    'subscribed',
    'unapproved',
)


def threads_list_patterns(prefix, view, patterns):
    urls = []
    for i, pattern in enumerate(patterns):
        if i > 0:
            url_name = '%s-%s' % (prefix, LISTS_TYPES[i])
        else:
            url_name = prefix

        urls.append(url(
            pattern,
            view.as_view(),
            name=url_name,
            kwargs={'list_type': LISTS_TYPES[i]},
        ))
    return urls


if settings.MISAGO_THREADS_ON_INDEX:
    urlpatterns = threads_list_patterns('threads', ForumThreads, (
        r'^$',
        r'^my/$',
        r'^new/$',
        r'^unread/$',
        r'^subscribed/$',
        r'^unapproved/$',
    ))
else:
    urlpatterns = threads_list_patterns('threads', ForumThreads, (
        r'^threads/$',
        r'^threads/my/$',
        r'^threads/new/$',
        r'^threads/unread/$',
        r'^threads/subscribed/$',
        r'^threads/unapproved/$',
    ))


urlpatterns += threads_list_patterns('category', CategoryThreads, (
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/$',
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/my/$',
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/new/$',
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/unread/$',
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/subscribed/$',
    r'^category/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/unapproved/$',
))


urlpatterns += threads_list_patterns('private-threads', CategoryThreads, (
    r'^private-threads/$',
    r'^private-threads/my/$',
    r'^private-threads/new/$',
    r'^private-threads/unread/$',
    r'^private-threads/subscribed/$',
    r'^private-threads/unapproved/$',
))


def thread_view_patterns(prefix, view):
    urls = [
        url(r'^%s/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/$' % prefix, view.as_view(), name=prefix),
        url(r'^%s/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/(?P<page>\d+)/$' % prefix, view.as_view(), name=prefix),
    ]
    return urls


urlpatterns += thread_view_patterns('thread', Thread)
urlpatterns += thread_view_patterns('private-thread', PrivateThread)


def goto_patterns(prefix, **views):
    urls = []

    post_view = views.pop('post', None)
    if post_view:
        url_pattern = r'^%s/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/post/(?P<post>\d+)/$' % prefix
        url_name = '%s-post' % prefix
        urls.append(url(url_pattern, post_view.as_view(), name=url_name))

    for name, view in views.items():
        url_pattern = r'^%s/(?P<slug>[-a-zA-Z0-9]+)-(?P<pk>\d+)/%s/$' % (prefix, name)
        url_name = '%s-%s' % (prefix, name)
        urls.append(url(url_pattern, view.as_view(), name=url_name))

    return urls


urlpatterns += goto_patterns(
    'thread',
    post=ThreadGotoPostView,
    last=ThreadGotoLastView,
    new=ThreadGotoNewView,
    unapproved=ThreadGotoUnapprovedView
)

urlpatterns += goto_patterns(
    'private-thread',
    post=ThreadGotoPostView,
    last=ThreadGotoLastView,
    new=ThreadGotoNewView,
    unapproved=ThreadGotoUnapprovedView
)


urlpatterns += [
    url(r'^attachment/(?P<secret>[-a-zA-Z0-9]+)-(?P<pk>\d+)/', attachment_server, name='attachment'),
    url(r'^attachment/thumb/(?P<secret>[-a-zA-Z0-9]+)-(?P<pk>\d+)/', attachment_server, name='attachment-thumbnail', kwargs={'thumbnail': True}),
]
