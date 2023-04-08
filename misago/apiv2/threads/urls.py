from django.urls import path

from .watch import watch_private_thread, watch_thread

urlpatterns = [
    path(
        "/private-threads/<int:thread_id>/watch/",
        watch_private_thread,
        name="private-thread-watch",
    ),
    path("/threads/<int:thread_id>/watch/", watch_thread, name="thread-watch"),
]
