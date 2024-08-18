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
from ..views.list import category_threads, private_threads, threads
from ..views.replies import private_thread_replies, thread_replies
from ..views.subscribed import redirect_subscribed_to_watched


urlpatterns = [
    path(
        "threads/",
        threads,
        name="threads",
        kwargs={"is_index": False},
    ),
    path(
        "threads/<slug:filter>/",
        threads,
        name="threads",
    ),
    path(
        "c/<slug:slug>/<int:id>/",
        category_threads,
        name="category",
    ),
    path(
        "c/<slug:slug>/<int:id>/<slug:filter>/",
        category_threads,
        name="category",
    ),
    path(
        "private/",
        private_threads,
        name="private-threads",
    ),
    path(
        "private/<slug:filter>/",
        private_threads,
        name="private-threads",
    ),
    path(
        "t/<slug:slug>/<int:id>/",
        thread_replies,
        name="thread",
    ),
    path(
        "t/<slug:slug>/<int:id>/<int:page>/",
        thread_replies,
        name="thread",
    ),
    path(
        "p/<slug:slug>/<int:id>/",
        private_thread_replies,
        name="private-thread",
    ),
    path(
        "p/<slug:slug>/<int:id>/<int:page>/",
        private_thread_replies,
        name="private-thread",
    ),
]


# Redirect from subscribed to watched
if settings.MISAGO_THREADS_ON_INDEX:
    root_subscribed_path = "subscribed/"
else:
    root_subscribed_path = "threads/subscribed/"

urlpatterns += [
    path(root_subscribed_path, redirect_subscribed_to_watched),
    path("c/<slug:slug>/<int:pk>/subscribed/", redirect_subscribed_to_watched),
    path("private-threads/subscribed/", redirect_subscribed_to_watched),
]


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
