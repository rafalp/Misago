from django.urls import path

from ..plugins import extensions
from .views import (
    EventDeleteView,
    EventHideView,
    EventUnhideView,
    # EventDeleteView,
    # ThreadEventHideView,
    # ThreadEventUnhideView,
)

private_thread_event_delete_view = extensions.get(
    EventDeleteView
).as_view()
private_thread_event_hide_view = extensions.get(EventHideView).as_view()
private_thread_event_unhide_view = extensions.get(
    EventUnhideView
).as_view()
thread_event_delete_view = extensions.get(EventDeleteView).as_view()
thread_event_hide_view = extensions.get(EventHideView).as_view()
thread_event_unhide_view = extensions.get(EventUnhideView).as_view()

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/hide/",
        thread_event_hide_view,
        name="thread-event-hide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/unhide/",
        thread_event_unhide_view,
        name="thread-event-unhide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/delete/",
        thread_event_delete_view,
        name="thread-event-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/hide/",
        private_thread_event_hide_view,
        name="private-thread-event-hide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/unhide/",
        private_thread_event_unhide_view,
        name="private-thread-event-unhide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/event/<int:thread_event_id>/delete/",
        private_thread_event_delete_view,
        name="private-thread-event-delete",
    ),
]
