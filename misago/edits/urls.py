from django.urls import path

from ..auth.decorators import login_required
from ..privatethreads.decorators import private_threads_login_required
from .views import (
    ThreadPostEditDeleteView,
    ThreadPostEditHideView,
    ThreadPostEditRestoreView,
    ThreadPostEditUnhideView,
    ThreadPostEditsView,
    PrivateThreadPostEditDeleteView,
    PrivateThreadPostEditHideView,
    PrivateThreadPostEditRestoreView,
    PrivateThreadPostEditUnhideView,
    PrivateThreadPostEditsView,
)


urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        ThreadPostEditsView.as_view(),
        name="thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        ThreadPostEditsView.as_view(),
        name="thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/restore/",
        login_required(ThreadPostEditRestoreView.as_view()),
        name="thread-post-edit-restore",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/hide/",
        login_required(ThreadPostEditHideView.as_view()),
        name="thread-post-edit-hide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/unhide/",
        login_required(ThreadPostEditUnhideView.as_view()),
        name="thread-post-edit-unhide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/delete/",
        login_required(ThreadPostEditDeleteView.as_view()),
        name="thread-post-edit-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        private_threads_login_required(PrivateThreadPostEditsView.as_view()),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        private_threads_login_required(PrivateThreadPostEditsView.as_view()),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/restore/",
        private_threads_login_required(PrivateThreadPostEditRestoreView.as_view()),
        name="private-thread-post-edit-restore",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/hide/",
        private_threads_login_required(PrivateThreadPostEditHideView.as_view()),
        name="private-thread-post-edit-hide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/unhide/",
        private_threads_login_required(PrivateThreadPostEditUnhideView.as_view()),
        name="private-thread-post-edit-unhide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/delete/",
        private_threads_login_required(PrivateThreadPostEditDeleteView.as_view()),
        name="private-thread-post-edit-delete",
    ),
]
