from django.urls import path

from .views.detail import ThreadDetailView
from .views.list import category_threads, threads
from .views.post import (
    ThreadPostLastView,
    ThreadPostSolutionView,
    ThreadPostUnapprovedView,
    ThreadPostUnreadView,
    ThreadPostView,
)

urlpatterns = [
    path(
        "threads/",
        threads,
        name="threads",
        kwargs={"is_index": False},
    ),
    path(
        "threads/<slug:filter>/",
        threads,
        name="threads",
    ),
    path(
        "c/<slug:slug>/<int:category_id>/",
        category_threads,
        name="category",
    ),
    path(
        "c/<slug:slug>/<int:category_id>/<slug:filter>/",
        category_threads,
        name="category",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/",
        ThreadDetailView.as_view(),
        name="thread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/<int:page>/",
        ThreadDetailView.as_view(),
        name="thread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/",
        ThreadPostView.as_view(),
        name="thread-post",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/last/",
        ThreadPostLastView.as_view(),
        name="thread-post-last",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/unapproved/",
        ThreadPostUnapprovedView.as_view(),
        name="thread-post-unapproved",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/unread/",
        ThreadPostUnreadView.as_view(),
        name="thread-post-unread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/solution/",
        ThreadPostSolutionView.as_view(),
        name="thread-post-solution",
    ),
]
