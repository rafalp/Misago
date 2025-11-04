from django.conf import settings
from django.http import HttpRequest

from ..threads.models import Post
from .hooks import synchronize_post_likes_hook
from .models import Like


def synchronize_post_likes(
    post: Post, commit: bool = True, request: HttpRequest | None = None
):
    synchronize_post_likes_hook(_synchronize_post_likes_action, post, commit, request)


def _synchronize_post_likes_action(
    post: Post, commit: bool = True, request: HttpRequest | None = None
):
    queryset = Like.objects.filter(post=post)

    post.likes = queryset.count()

    if post.likes:
        last_likes_queryset = queryset.values("user_id", "user_name").order_by("-id")[
            : settings.MISAGO_POST_LAST_LIKES_LIMIT
        ]

        post.last_likes = [
            {"id": user["user_id"], "username": user["user_name"]}
            for user in last_likes_queryset
        ]
    else:
        post.last_likes = None

    if commit:
        post.save(update_fields=["likes", "last_likes"])
