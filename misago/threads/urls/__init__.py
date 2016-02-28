from django.conf import settings
from django.conf.urls import patterns, url

from misago.threads.views.threadslist import (
    ThreadsList, CategoryThreadsList, PrivateThreadsList)


PATTERNS_KWARGS = (
    {'list_type': 'all'},
    {'list_type': 'my'},
    {'list_type': 'new'},
    {'list_type': 'unread'},
    {'list_type': 'subscribed'},
)


def threads_list_patterns(root_name, view, patterns):
    urlpatterns = []

    for i, pattern in enumerate(patterns):
        if i > 0:
            url_name = '%s_%s' % (root_name, PATTERNS_KWARGS[i]['list_type'])
        else:
            url_name = root_name

        urlpatterns.append(url(
            pattern,
            view.as_view(),
            name=url_name,
            kwargs=PATTERNS_KWARGS[i],
        ))

    return urlpatterns


if settings.MISAGO_CATEGORIES_ON_INDEX:
    urlpatterns = threads_list_patterns('threads', ThreadsList, (
        r'^threads/$',
        r'^threads/my/$',
        r'^threads/new/$',
        r'^threads/unread/$',
        r'^threads/subscribed/$',
    ))
else:
    urlpatterns = threads_list_patterns('threads', ThreadsList, (
        r'^$',
        r'^my/$',
        r'^new/$',
        r'^unread/$',
        r'^subscribed/$',
    ))


urlpatterns += threads_list_patterns('category', CategoryThreadsList, (
    r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/$',
    r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/my/$',
    r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/new/$',
    r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/unread/$',
    r'^category/(?P<category_slug>[-a-zA-Z0-9]+)-(?P<category_id>\d+)/subscribed/$',
))


urlpatterns += threads_list_patterns('private_threads', CategoryThreadsList, (
    r'^private-threads/$',
    r'^private-threads/my/$',
    r'^private-threads/new/$',
    r'^private-threads/unread/$',
    r'^private-threads/subscribed/$',
))