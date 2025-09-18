from django.urls import path

from .views import (
    CloseThreadPollView,
    DeleteThreadPollView,
    EditThreadPollView,
    OpenThreadPollView,
    StartThreadPollView,
)

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/poll/start/",
        StartThreadPollView.as_view(),
        name="thread-poll-start",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/poll/edit/",
        EditThreadPollView.as_view(),
        name="thread-poll-edit",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/poll/close/",
        CloseThreadPollView.as_view(),
        name="thread-poll-close",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/poll/open/",
        OpenThreadPollView.as_view(),
        name="thread-poll-open",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/poll/delete/",
        DeleteThreadPollView.as_view(),
        name="thread-poll-delete",
    ),
]
