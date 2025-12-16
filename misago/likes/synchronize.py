from django.conf import settings
from django.db.models import QuerySet
from django.http import HttpRequest

from ..threads.models import Post
from .hooks import synchronize_post_likes_hook
from .models import Like


def synchronize_post_likes(
    post: Post,
    queryset: QuerySet | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    synchronize_post_likes_hook(
        _synchronize_post_likes_action, post, queryset, commit, request
    )


def _synchronize_post_likes_action(
    post: Post,
    queryset: QuerySet | None = None,
    commit: bool = True,
    request: HttpRequest | None = None,
):
    queryset = (queryset or Like.objects).filter(post=post)
    post.likes = queryset.count()

    if post.likes:
        last_likes_queryset = queryset.values("user_id", "user_name").order_by("-id")
        post.last_likes = [
            {"id": user["user_id"], "username": user["user_name"]}
            for user in last_likes_queryset[: settings.MISAGO_POST_LAST_LIKES_LIMIT]
        ]
    else:
        post.last_likes = None

    if commit:
        post.save(update_fields=["likes", "last_likes"])
