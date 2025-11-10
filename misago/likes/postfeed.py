from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.utils.translation import npgettext, pgettext

from ..permissions.checkutils import check_permissions
from ..permissions.likes import can_see_post_likes_count, check_like_post_permission, check_see_post_likes_permission, check_unlike_post_permission
from ..threads.models import Post

if TYPE_CHECKING:
    from ..users.models import User


def get_post_feed_post_likes_data(request: HttpRequest, post: Post, is_liked: bool, like_url: str, unlike_url: str) -> dict:
    return _get_post_feed_post_likes_data_action(request, post, is_liked, like_url, unlike_url)


def _get_post_feed_post_likes_data_action(request: HttpRequest, post: Post, is_liked: bool, like_url: str, unlike_url: str) -> dict:
    data = {
        "likes": None,
        "description": None,
        "is_liked": is_liked,
        "like_url": None,
        "unlike_url": None,
    }

    if can_see_post_likes_count(request.user_permissions, post.category, post.thread, post):
        data["likes"] = post.likes

    if post.likes and post.last_likes:
        with check_permissions():
            check_see_post_likes_permission(request.user_permissions, post.category, post.thread, post)
            data["description"] = {
                "short": get_post_likes_description(request.user, post, is_liked, 5),
                "medium": get_post_likes_description(request.user, post, is_liked, 10),
                "long": get_post_likes_description(request.user, post, is_liked, 20),
            }

    with check_permissions():
        check_like_post_permission(request.user_permissions, post.category, post.thread, post)
        data["like_url"] = like_url

    with check_permissions():
        check_unlike_post_permission(request.user_permissions, post.category, post.thread, post)
        data["unlike_url"] = unlike_url

    return data


def get_post_likes_description(user: Union["User", AnonymousUser], post: Post, is_liked: bool, length: int | None = None) -> str:
    if post.likes == 1:
        if is_liked:
            return pgettext("post likes description", "You like this.")
        else:
            return pgettext("post likes description", "%(user)s likes this.") % {
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
        return pgettext("post likes description", "%(former)s and %(latter)s like this.") % {
            "former": last_users[0],
            "latter": last_users[1],
        }
    
    if remaining_likes:
        return pgettext("post likes description", "%(users)s, +%(extra)s like this.") % {
            "users": ", ".join(last_users),
            "extra": remaining_likes,
        }

    return pgettext("post likes description", "%(users)s and %(last)s like this.") % {
        "users": ", ".join(last_users[:-1]),
        "last": last_users[-1],
    }
