from django.urls import path

from .views import (
    PollCloseView,
    PollDeleteView,
    PollEditView,
    PollOpenView,
    PollStartView,
)

urlpatterns = [
    path(
        "t/<slug:slug>/<int:id>/poll/start/",
        PollStartView.as_view(),
        name="start-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/edit/",
        PollEditView.as_view(),
        name="edit-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/close/",
        PollCloseView.as_view(),
        name="close-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/open/",
        PollOpenView.as_view(),
        name="open-thread-poll",
    ),
    path(
        "t/<slug:slug>/<int:id>/poll/delete/",
        PollDeleteView.as_view(),
        name="delete-thread-poll",
    ),
]
