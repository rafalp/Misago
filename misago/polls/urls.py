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
        "t/<slug:slug>/<int:id>/poll/start/",
        StartThreadPollView.as_view(),
        name="thread-poll-start",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/edit/",
        EditThreadPollView.as_view(),
        name="thread-poll-edit",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/close/",
        CloseThreadPollView.as_view(),
        name="thread-poll-close",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/open/",
        OpenThreadPollView.as_view(),
        name="thread-poll-open",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/delete/",
        DeleteThreadPollView.as_view(),
        name="thread-poll-delete",
    ),
]
