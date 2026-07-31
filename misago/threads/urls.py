from django.urls import path

from ..plugins.extensions import extensions
from .views import (
    CategoryThreadListView,
    ThreadDetailView,
    ThreadListView,
    ThreadPostLastView,
    ThreadPostSolutionView,
    ThreadPostUnapprovedView,
    ThreadPostUnreadView,
    ThreadPostView,
    post,
)

thread_list_view = extensions.get(ThreadListView).as_view()
category_thread_list_view = extensions.get(CategoryThreadListView).as_view()
thread_detail_view = extensions.get(ThreadDetailView).as_view()
thread_post_view = extensions.get(ThreadPostView).as_view()
thread_post_last_view = extensions.get(ThreadPostLastView).as_view()
thread_post_unapproved_view = extensions.get(ThreadPostUnapprovedView).as_view()
thread_post_unread_view = extensions.get(ThreadPostUnreadView).as_view()
thread_post_solution_view = extensions.get(ThreadPostSolutionView).as_view()

urlpatterns = [
    path("post/<int:post_id>/", post, name="post"),
    path(
        "threads/",
        thread_list_view,
        name="thread-list",
        kwargs={"is_index": False},
    ),
    path(
        "threads/<slug:filter>/",
        thread_list_view,
        name="thread-list",
    ),
    path(
        "c/<slug:slug>/<int:category_id>/",
        category_thread_list_view,
        name="category-thread-list",
    ),
    path(
        "c/<slug:slug>/<int:category_id>/<slug:filter>/",
        category_thread_list_view,
        name="category-thread-list",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/",
        thread_detail_view,
        name="thread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/<int:page>/",
        thread_detail_view,
        name="thread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/",
        thread_post_view,
        name="thread-post",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/last/",
        thread_post_last_view,
        name="thread-post-last",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/unapproved/",
        thread_post_unapproved_view,
        name="thread-post-unapproved",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/unread/",
        thread_post_unread_view,
        name="thread-post-unread",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/solution/",
        thread_post_solution_view,
        name="thread-post-solution",
    ),
]
