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
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/",
        ThreadPostLikesView.as_view(),
        name="thread-post-likes",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/<int:page>/",
        ThreadPostLikesView.as_view(),
        name="thread-post-likes",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/like/",
        ThreadPostLikeView.as_view(),
        name="thread-post-like",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/unlike/",
        ThreadPostUnlikeView.as_view(),
        name="thread-post-unlike",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/",
        PrivateThreadPostLikesView.as_view(),
        name="private-thread-post-likes",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/<int:page>/",
        PrivateThreadPostLikesView.as_view(),
        name="private-thread-post-likes",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/like/",
        PrivateThreadPostLikeView.as_view(),
        name="private-thread-post-like",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/unlike/",
        PrivateThreadPostUnlikeView.as_view(),
        name="private-thread-post-unlike",
    ),
]
