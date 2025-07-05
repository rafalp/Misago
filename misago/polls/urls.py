from django.urls import path

from .views import poll_start

urlpatterns = [
    path(
        "t/<slug:slug>/<int:id>/start-pool/",
        poll_start,
        name="start-thread-poll",
    ),
]