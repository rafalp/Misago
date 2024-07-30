from django.urls import path

from .views.start import (
    PrivateThreadStartView,
    ThreadStartSelectCategoryView,
    ThreadStartView,
)


urlpatterns = [
    path(
        "start-thread/",
        ThreadStartSelectCategoryView.as_view(),
        name="start-thread",
    ),
    path(
        "c/<slug:slug>/<int:id>/start-thread/",
        ThreadStartView.as_view(),
        name="start-thread",
    ),
    path(
        "private/start-thread/",
        PrivateThreadStartView.as_view(),
        name="start-private-thread",
    ),
]
