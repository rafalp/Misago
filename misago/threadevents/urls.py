from django.urls import path

from .views import (
    PrivateThreadEventDeleteView,
    PrivateThreadEventHideView,
    PrivateThreadEventUnhideView,
    ThreadEventDeleteView,
    ThreadEventHideView,
    ThreadEventUnhideView,
)

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/hide/",
        ThreadEventHideView.as_view(),
        name="thread-event-hide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/unhide/",
        ThreadEventUnhideView.as_view(),
        name="thread-event-unhide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/delete/",
        ThreadEventDeleteView.as_view(),
        name="thread-event-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/hide/",
        PrivateThreadEventHideView.as_view(),
        name="private-thread-event-hide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/unhide/",
        PrivateThreadEventUnhideView.as_view(),
        name="private-thread-event-unhide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/delete/",
        PrivateThreadEventDeleteView.as_view(),
        name="private-thread-event-delete",
    ),
]
