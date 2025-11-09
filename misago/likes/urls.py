from django.urls import path

from .views import (
    ThreadPostLikesView,
    ThreadPostLikeView,
    ThreadPostUnlikeView,
    PrivateThreadPostLikesView,
    PrivateThreadPostLikeView,
    PrivateThreadPostUnlikeView,
)


urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/likes/<int:post_id>/",
        ThreadPostLikesView.as_view(),
        name="thread-post-likes",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/like/<int:post_id>/",
        ThreadPostLikeView.as_view(),
        name="thread-post-like",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/unlike/<int:post_id>/",
        ThreadPostUnlikeView.as_view(),
        name="thread-post-unlike",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/likes/<int:post_id>/",
        PrivateThreadPostLikesView.as_view(),
        name="private-thread-post-likes",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/like/<int:post_id>/",
        PrivateThreadPostLikeView.as_view(),
        name="private-thread-post-like",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/unlike/<int:post_id>/",
        PrivateThreadPostUnlikeView.as_view(),
        name="private-thread-post-unlike",
    ),
]
