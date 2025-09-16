from django.urls import path

from .views import (
    PrivateThreadUpdateDeleteView,
    PrivateThreadUpdateHideView,
    PrivateThreadUpdateUnhideView,
    ThreadUpdateDeleteView,
    ThreadUpdateHideView,
    ThreadUpdateUnhideView,
)

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/hide/",
        ThreadUpdateHideView.as_view(),
        name="thread-update-hide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/unhide/",
        ThreadUpdateUnhideView.as_view(),
        name="thread-update-unhide",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/delete/",
        ThreadUpdateDeleteView.as_view(),
        name="thread-update-delete",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/hide/",
        PrivateThreadUpdateHideView.as_view(),
        name="private-thread-update-hide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/unhide/",
        PrivateThreadUpdateUnhideView.as_view(),
        name="private-thread-update-unhide",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/update/<int:thread_update_id>/delete/",
        PrivateThreadUpdateDeleteView.as_view(),
        name="private-thread-update-delete",
    ),
]
