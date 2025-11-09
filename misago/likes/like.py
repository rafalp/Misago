from typing import TYPE_CHECKING, Union

from django.conf import settings
from django.http import HttpRequest

from ..core.utils import slugify
from ..threads.models import Post
from .hooks import like_post_hook, remove_post_like_hook
from .models import Like
from .synchronize import synchronize_post_likes

if TYPE_CHECKING:
    from ..users.models import User


def like_post(
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Like:
    return like_post_hook(_like_post_action, post, user, commit, request)


def _like_post_action(
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
) -> Like:
    if isinstance(user, str):
        user_id = None
        user_name = user
        user_slug = slugify(user)
        user = None
    else:
        user_id = user.id
        user_name = user.username
        user_slug = user.slug

    like = Like(
        category=post.category,
        thread=post.thread,
        post=post,
        user=user,
        user_name=user_name,
        user_slug=user_slug,
    )

    last_like = {"id": user_id, "username": user_name}

    post.likes += 1
    if post.last_likes:
        post.last_likes.insert(0, last_like)
        post.last_likes = post.last_likes[: settings.MISAGO_POST_LAST_LIKES_LIMIT]
    else:
        post.last_likes = [last_like]

    if commit:
        like.save()
        post.save(update_fields=["likes", "last_likes"])

    return like


def remove_post_like(
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    return remove_post_like_hook(_remove_post_like_action, post, user, commit, request)


def _remove_post_like_action(
    post: Post,
    user: Union["User", str],
    commit: bool = True,
    request: HttpRequest | None = None,
):
    Like.objects.filter(post=post, user=user).delete()
    synchronize_post_likes(post, commit, request)
