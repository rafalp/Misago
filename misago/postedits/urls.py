from django.urls import path

from ..auth.decorators import login_required
from ..plugins import extensions
from ..privatethreads.decorators import private_threads_login_required
from .views import (
    PrivateThreadPostEditDeleteView,
    PrivateThreadPostEditHideView,
    PrivateThreadPostEditRestoreView,
    PrivateThreadPostEditsView,
    PrivateThreadPostEditUnhideView,
    ThreadPostEditDeleteView,
    ThreadPostEditHideView,
    ThreadPostEditRestoreView,
    ThreadPostEditsView,
    ThreadPostEditUnhideView,
)

private_thread_post_edit_delete_view = extensions.get(
    PrivateThreadPostEditDeleteView
).as_view()
private_thread_post_edit_hide_view = extensions.get(
    PrivateThreadPostEditHideView
).as_view()
private_thread_post_edit_restore_view = extensions.get(
    PrivateThreadPostEditRestoreView
).as_view()
private_thread_post_edits_view = extensions.get(PrivateThreadPostEditsView).as_view()
private_thread_post_edit_unhide_view = extensions.get(
    PrivateThreadPostEditUnhideView
).as_view()
thread_post_edit_delete_view = extensions.get(ThreadPostEditDeleteView).as_view()
thread_post_edit_hide_view = extensions.get(ThreadPostEditHideView).as_view()
thread_post_edit_restore_view = extensions.get(ThreadPostEditRestoreView).as_view()
thread_post_edits_view = extensions.get(ThreadPostEditsView).as_view()
thread_post_edit_unhide_view = extensions.get(ThreadPostEditUnhideView).as_view()

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        thread_post_edits_view,
        name="thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        thread_post_edits_view,
        name="thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/restore/",
        login_required(thread_post_edit_restore_view),
        name="thread-post-edit-restore",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/hide/",
        login_required(thread_post_edit_hide_view),
        name="thread-post-edit-hide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/unhide/",
        login_required(thread_post_edit_unhide_view),
        name="thread-post-edit-unhide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/delete/",
        login_required(thread_post_edit_delete_view),
        name="thread-post-edit-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        private_threads_login_required(private_thread_post_edits_view),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        private_threads_login_required(private_thread_post_edits_view),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/restore/",
        private_threads_login_required(private_thread_post_edit_restore_view),
        name="private-thread-post-edit-restore",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/hide/",
        private_threads_login_required(private_thread_post_edit_hide_view),
        name="private-thread-post-edit-hide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/unhide/",
        private_threads_login_required(private_thread_post_edit_unhide_view),
        name="private-thread-post-edit-unhide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:post_edit_id>/delete/",
        private_threads_login_required(private_thread_post_edit_delete_view),
        name="private-thread-post-edit-delete",
    ),
]
