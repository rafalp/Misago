from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from ..permissions.checkutils import check_permissions
from ..permissions.likes import (
    can_see_post_likes_count,
    check_like_post_permission,
    check_see_post_likes_permission,
    check_unlike_post_permission,
)
from ..threads.models import Post
from .hooks import get_post_feed_post_likes_data_hook

if TYPE_CHECKING:
    from ..users.models import User


def get_post_feed_post_likes_data(
    request: HttpRequest,
    post: Post,
    is_liked: bool,
    likes_url: str,
    like_url: str,
    unlike_url: str,
) -> dict:
    return get_post_feed_post_likes_data_hook(
        _get_post_feed_post_likes_data_action,
        request,
        post,
        is_liked,
        likes_url,
        like_url,
        unlike_url,
    )


def _get_post_feed_post_likes_data_action(
    request: HttpRequest,
    post: Post,
    is_liked: bool,
    likes_url: str,
    like_url: str,
    unlike_url: str,
) -> dict:
    data = {
        "likes": None,
        "description": None,
        "is_liked": is_liked,
        "likes_url": None,
        "like_url": None,
        "unlike_url": None,
    }

    show_likes_count = False
    show_last_likes = False

    if can_see_post_likes_count(
        request.user_permissions, post.category, post.thread, post
    ):
        show_likes_count = True

    with check_permissions() as show_last_likes:
        check_see_post_likes_permission(
            request.user_permissions, post.category, post.thread, post
        )

    if show_likes_count:
        data["likes"] = post.likes

    if show_last_likes and post.likes:
        data["likes_url"] = likes_url

    if is_liked:
        data["description"] = {
            "liked": pgettext("post likes description", "You like this"),
        }

    if not is_liked or post.likes > 1:
        if show_last_likes and post.last_likes:
            data["description"] = {
                "short": get_post_likes_description(request.user, post, is_liked, 5),
                "medium": get_post_likes_description(request.user, post, is_liked, 10),
                "long": get_post_likes_description(request.user, post, is_liked, 20),
            }

        elif show_likes_count and post.likes:
            data["description"] = {
                "count": get_post_likes_count_description(post, is_liked),
            }

    with check_permissions():
        check_like_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        data["like_url"] = like_url

    with check_permissions():
        check_unlike_post_permission(
            request.user_permissions, post.category, post.thread, post
        )
        data["unlike_url"] = unlike_url

    return data


def get_post_likes_count_description(
    post: Post,
    is_liked: bool,
) -> str:
    if is_liked:
        likes = post.likes - 1
        return npgettext(
            "post likes description",
            "You and %(likes)s other like this",
            "You and %(likes)s others like this",
            likes,
        ) % {"likes": likes}

    return npgettext(
        "post likes description",
        "%(likes)s other likes this",
        "%(likes)s others like this",
        post.likes,
    ) % {"likes": post.likes}


def get_post_likes_description(
    user: Union["User", AnonymousUser],
    post: Post,
    is_liked: bool,
    length: int | None = None,
) -> str:
    if post.likes == 1:
        if is_liked:
            return pgettext("post likes description", "You like this")

        return pgettext("post likes description", "%(user)s likes this") % {
            "user": post.last_likes[0]["username"]
        }

    remaining_likes = post.likes
    last_likes = post.last_likes[:length] if length else post.last_likes[:length]

    if user.is_anonymous:
        last_users = [like["username"] for like in last_likes]
    else:
        last_users = [like["username"] for like in last_likes if like["id"] != user.id]

    if is_liked:
        last_users.insert(0, pgettext("post likes description", "You"))

    remaining_likes = max(remaining_likes - len(last_users), 0)

    if len(last_users) == 2:
        return pgettext(
            "post likes description", "%(former)s and %(latter)s like this"
        ) % {
            "former": last_users[0],
            "latter": last_users[1],
        }

    if remaining_likes:
        return npgettext(
            "post likes description",
            "%(users)s and %(likes)s other like this",
            "%(users)s and %(likes)s others like this",
            remaining_likes,
        ) % {
            "users": ", ".join(last_users),
            "likes": remaining_likes,
        }

    return pgettext("post likes description", "%(users)s and %(last)s like this.") % {
        "users": ", ".join(last_users[:-1]),
        "last": last_users[-1],
    }
