from django.urls import path

from .views import (
    ThreadPostEditsView,
    ThreadPostRestoreView,
    PrivateThreadPostEditsView,
    PrivateThreadPostRestoreView,
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
        ThreadPostRestoreView.as_view(),
        name="thread-post-restore",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/",
        PrivateThreadPostEditsView.as_view(),
        name="private-thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/edits/<int:page>/",
        PrivateThreadPostEditsView.as_view(),
        name="private-thread-post-edits",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/restore/<int:post_edit_id>/",
        PrivateThreadPostRestoreView.as_view(),
        name="private-thread-post-restore",
    ),
]
