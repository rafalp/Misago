from django.urls import path

from .views import PollDeleteView, PollEditView, PollStartView

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
        "t/<slug:slug>/<int:id>/poll/delete/",
        PollDeleteView.as_view(),
        name="delete-thread-poll",
    ),
]
