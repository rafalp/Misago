from django.urls import path

from ..plugins import extensions
from ..privatethreads.decorators import private_threads_login_required
from .views import (
    PrivateThreadPostLikesView,
    PrivateThreadPostLikeView,
    PrivateThreadPostUnlikeView,
    ThreadPostLikesView,
    ThreadPostLikeView,
    ThreadPostUnlikeView,
)

thread_post_likes_view = extensions.get(ThreadPostLikesView).as_view()
thread_post_like_view = extensions.get(ThreadPostLikeView).as_view()
thread_post_unlike_view = extensions.get(ThreadPostUnlikeView).as_view()
private_thread_post_likes_view = extensions.get(PrivateThreadPostLikesView).as_view()
private_thread_post_like_view = extensions.get(PrivateThreadPostLikeView).as_view()
private_thread_post_unlike_view = extensions.get(PrivateThreadPostUnlikeView).as_view()

urlpatterns = [
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/",
        thread_post_likes_view,
        name="thread-post-likes",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/<int:page>/",
        thread_post_likes_view,
        name="thread-post-likes",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/like/",
        thread_post_like_view,
        name="thread-post-like",
    ),
    path(
        "t/<slug:slug>/<int:thread_id>/post/<int:post_id>/unlike/",
        thread_post_unlike_view,
        name="thread-post-unlike",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/",
        private_threads_login_required(private_thread_post_likes_view),
        name="private-thread-post-likes",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/likes/<int:page>/",
        private_threads_login_required(private_thread_post_likes_view),
        name="private-thread-post-likes",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/like/",
        private_thread_post_like_view,
        name="private-thread-post-like",
    ),
    path(
        "p/<slug:slug>/<int:thread_id>/post/<int:post_id>/unlike/",
        private_thread_post_unlike_view,
        name="private-thread-post-unlike",
    ),
]
