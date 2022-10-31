from django.urls import path

from ...conf import settings

from ..views.attachment import attachment_server
from ..views.goto import (
    ThreadGotoPostView,
    ThreadGotoLastView,
    ThreadGotoNewView,
    ThreadGotoBestAnswerView,
    ThreadGotoUnapprovedView,
    PrivateThreadGotoPostView,
    PrivateThreadGotoLastView,
    PrivateThreadGotoNewView,
)
from ..views.list import ForumThreadsList, CategoryThreadsList, PrivateThreadsList
from ..views.thread import ThreadView, PrivateThreadView

LISTS_TYPES = ("all", "my", "new", "unread", "subscribed", "unapproved")


def threads_list_patterns(prefix, view, patterns):
    urls = []
    for i, pattern in enumerate(patterns):
        if i > 0:
            url_name = "%s-%s" % (prefix, LISTS_TYPES[i])
        else:
            url_name = prefix

        urls.append(
            path(
                pattern,
                view.as_view(),
                name=url_name,
                kwargs={"list_type": LISTS_TYPES[i]},
            )
        )
    return urls


if settings.MISAGO_THREADS_ON_INDEX:
    urlpatterns = threads_list_patterns(
        "threads",
        ForumThreadsList,
        ("", "my/", "new/", "unread/", "subscribed/", "unapproved/"),
    )
else:
    urlpatterns = threads_list_patterns(
        "threads",
        ForumThreadsList,
        (
            "threads/",
            "threads/my/",
            "threads/new/",
            "threads/unread/",
            "threads/subscribed/",
            "threads/unapproved/",
        ),
    )

urlpatterns += threads_list_patterns(
    "category",
    CategoryThreadsList,
    (
        "c/<slug:slug>/<int:pk>/",
        "c/<slug:slug>/<int:pk>/my/",
        "c/<slug:slug>/<int:pk>/new/",
        "c/<slug:slug>/<int:pk>/unread/",
        "c/<slug:slug>/<int:pk>/subscribed/",
        "c/<slug:slug>/<int:pk>/unapproved/",
    ),
)

urlpatterns += threads_list_patterns(
    "private-threads",
    PrivateThreadsList,
    (
        "private-threads/",
        "private-threads/my/",
        "private-threads/new/",
        "private-threads/unread/",
        "private-threads/subscribed/",
    ),
)


def thread_view_patterns(prefix, view):
    urls = [
        path(
            "%s/<slug:slug>/<int:pk>/" % prefix[0],
            view.as_view(),
            name=prefix,
        ),
        path(
            "%s/<slug:slug>/<int:pk>/<int:page>/" % prefix[0],
            view.as_view(),
            name=prefix,
        ),
    ]
    return urls


urlpatterns += thread_view_patterns("thread", ThreadView)
urlpatterns += thread_view_patterns("private-thread", PrivateThreadView)


def goto_patterns(prefix, **views):
    urls = []

    post_view = views.pop("post", None)
    if post_view:
        url_pattern = "%s/<slug:slug>/<int:pk>/post/<int:post>/" % prefix[0]
        url_name = "%s-post" % prefix
        urls.append(path(url_pattern, post_view.as_view(), name=url_name))

    for name, view in views.items():
        name = name.replace("_", "-")
        url_pattern = "%s/<slug:slug>/<int:pk>/%s/" % (
            prefix[0],
            name,
        )
        url_name = "%s-%s" % (prefix, name)
        urls.append(path(url_pattern, view.as_view(), name=url_name))

    return urls


urlpatterns += goto_patterns(
    "thread",
    post=ThreadGotoPostView,
    last=ThreadGotoLastView,
    new=ThreadGotoNewView,
    best_answer=ThreadGotoBestAnswerView,
    unapproved=ThreadGotoUnapprovedView,
)

urlpatterns += goto_patterns(
    "private-thread",
    post=PrivateThreadGotoPostView,
    last=PrivateThreadGotoLastView,
    new=PrivateThreadGotoNewView,
)

urlpatterns += [
    path(
        "a/<slug:secret>/<int:pk>/",
        attachment_server,
        name="attachment",
    ),
    path(
        "a/thumb/<slug:secret>/<int:pk>/",
        attachment_server,
        name="attachment-thumbnail",
        kwargs={"thumbnail": True},
    ),
]
