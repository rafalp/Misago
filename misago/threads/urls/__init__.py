from django.urls import path

from ...conf import settings

from ..views.attachment import attachment_server
from ..views.edit import (
    private_thread_edit,
    private_thread_edit_post,
    thread_edit,
    thread_edit_post,
)
from ..views.list import category_threads, private_threads, threads
from ..views.redirect import (
    PostRedirectView,
    PrivateThreadLastPostRedirectView,
    PrivateThreadUnapprovedPostRedirectView,
    PrivateThreadUnreadPostRedirectView,
    ThreadLastPostRedirectView,
    ThreadSolutionRedirectView,
    ThreadUnapprovedPostRedirectView,
    ThreadUnreadPostRedirectView,
)
from ..views.replies import private_thread_replies, thread_replies
from ..views.reply import private_thread_reply, thread_reply
from ..views.selectcategory import SelectCategoryView
from ..views.start import StartPrivateThreadView, StartThreadView
from ..views.subscribed import redirect_subscribed_to_watched


urlpatterns = [
    path(
        "start-thread/",
        SelectCategoryView.as_view(),
        name="start-thread",
    ),
    path(
        "c/<slug:slug>/<int:id>/start-thread/",
        StartThreadView.as_view(),
        name="start-thread",
    ),
    path(
        "private/start-thread/",
        StartPrivateThreadView.as_view(),
        name="start-private-thread",
    ),
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
    path(
        "t/<slug:slug>/<int:id>/last/",
        ThreadLastPostRedirectView.as_view(),
        name="thread-last-post",
    ),
    path(
        "t/<slug:slug>/<int:id>/unread/",
        ThreadUnreadPostRedirectView.as_view(),
        name="thread-unread-post",
    ),
    path(
        "t/<slug:slug>/<int:id>/unapproved/",
        ThreadUnapprovedPostRedirectView.as_view(),
        name="thread-unapproved-post",
    ),
    path(
        "t/<slug:slug>/<int:id>/solution/",
        ThreadSolutionRedirectView.as_view(),
        name="thread-solution-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/last/",
        PrivateThreadLastPostRedirectView.as_view(),
        name="private-thread-last-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/unread/",
        PrivateThreadUnreadPostRedirectView.as_view(),
        name="private-thread-unread-post",
    ),
    path(
        "p/<slug:slug>/<int:id>/unapproved/",
        PrivateThreadUnapprovedPostRedirectView.as_view(),
        name="private-thread-unapproved-post",
    ),
    path(
        "t/<slug:slug>/<int:id>/reply/",
        thread_reply,
        name="thread-reply",
    ),
    path(
        "p/<slug:slug>/<int:id>/reply/",
        private_thread_reply,
        name="private-thread-reply",
    ),
    path(
        "t/<slug:slug>/<int:id>/edit/",
        thread_edit,
        name="thread-edit",
    ),
    path(
        "p/<slug:slug>/<int:id>/edit/",
        private_thread_edit,
        name="private-thread-edit",
    ),
    path(
        "t/<slug:slug>/<int:id>/edit/<int:post>/",
        thread_edit_post,
        name="thread-edit",
    ),
    path(
        "p/<slug:slug>/<int:id>/edit/<int:post>/",
        private_thread_edit_post,
        name="private-thread-edit",
    ),
    path(
        "post/<int:id>/",
        PostRedirectView.as_view(),
        name="post",
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
