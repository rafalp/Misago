from django.urls import path

from .views import (
    ThreadPostEditDeleteView,
    ThreadPostEditRestoreView,
    ThreadPostEditsView,
    PrivateThreadPostEditDeleteView,
    PrivateThreadPostEditRestoreView,
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
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/restore/<int:post_edit_id>/",
        ThreadPostEditRestoreView.as_view(),
        name="thread-post-edit-restore",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/delete/<int:post_edit_id>/",
        ThreadPostEditDeleteView.as_view(),
        name="thread-post-edit-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        PrivateThreadPostEditsView.as_view(),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        PrivateThreadPostEditsView.as_view(),
        name="private-thread-post-edits",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/restore/<int:post_edit_id>/",
        PrivateThreadPostEditRestoreView.as_view(),
        name="private-thread-post-edit-restore",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/delete/<int:post_edit_id>/",
        PrivateThreadPostEditDeleteView.as_view(),
        name="private-thread-post-edit-delete",
    ),
]
