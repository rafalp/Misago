from django.urls import path

from .views import (
    ThreadSolutionClearView,
    ThreadSolutionLockView,
    ThreadSolutionSelectView,
    ThreadSolutionUnlockView,
)


urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/solution/select/<int:post_id>/",
        ThreadSolutionSelectView.as_view(),
        name="thread-solution-select",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/solution/clear/",
        ThreadSolutionClearView.as_view(),
        name="thread-solution-clear",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/solution/lock/",
        ThreadSolutionLockView.as_view(),
        name="thread-solution-lock",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/solution/unlock/",
        ThreadSolutionUnlockView.as_view(),
        name="thread-solution-unlock",
    ),
]
