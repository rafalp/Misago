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
        name="start-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/edit/",
        EditThreadPollView.as_view(),
        name="edit-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/close/",
        CloseThreadPollView.as_view(),
        name="close-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/open/",
        OpenThreadPollView.as_view(),
        name="open-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/delete/",
        DeleteThreadPollView.as_view(),
        name="delete-thread-poll",
    ),
]
