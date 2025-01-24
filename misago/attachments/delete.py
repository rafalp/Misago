from typing import TYPE_CHECKING, Iterable, Union

from django.db.models import Model
from django.http import HttpRequest

from ..categories.models import Category
from ..threads.models import Post, Thread
from .hooks import (
    delete_attachments_hook,
    delete_categories_attachments_hook,
    delete_posts_attachments_hook,
    delete_threads_attachments_hook,
    delete_users_attachments_hook,
)
from .models import Attachment

if TYPE_CHECKING:
    from ..users.models import User

__all__ = [
    "delete_attachments",
    "delete_categories_attachments",
    "delete_posts_attachments",
    "delete_threads_attachments",
    "delete_users_attachments",
]


def delete_categories_attachments(
    categories: Iterable[Union[Category, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return delete_categories_attachments_hook(
        _delete_categories_attachments_action, categories, request=request
    )


def _delete_categories_attachments_action(
    categories: Iterable[Union[Category, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return _update_queryset(
        Attachment.objects.filter(category_id__in=_flatten_ids_list(categories))
    )


def delete_threads_attachments(
    threads: Iterable[Union[Thread, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return delete_threads_attachments_hook(
        _delete_threads_attachments_action, threads, request=request
    )


def _delete_threads_attachments_action(
    threads: Iterable[Union[Thread, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return _update_queryset(
        Attachment.objects.filter(thread_id__in=_flatten_ids_list(threads))
    )


def delete_posts_attachments(
    posts: Iterable[Union[Post, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return delete_posts_attachments_hook(
        _delete_posts_attachments_action, posts, request=request
    )


def _delete_posts_attachments_action(
    posts: Iterable[Union[Post, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return _update_queryset(
        Attachment.objects.filter(post_id__in=_flatten_ids_list(posts))
    )


def delete_users_attachments(
    users: Iterable[Union["User", int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return delete_users_attachments_hook(
        _delete_users_attachments_action, users, request=request
    )


def _delete_users_attachments_action(
    users: Iterable[Union["User", int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return _update_queryset(
        Attachment.objects.filter(uploader_id__in=_flatten_ids_list(users))
    )


def delete_attachments(
    attachments: Iterable[Union[Attachment, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return delete_attachments_hook(
        _delete_attachments_action, attachments, request=request
    )


def _delete_attachments_action(
    attachments: Iterable[Union[Attachment, int]],
    *,
    request: HttpRequest | None = None,
) -> int:
    return _update_queryset(
        Attachment.objects.filter(id__in=_flatten_ids_list(attachments))
    )


def _flatten_ids_list(obs_or_ids: Iterable[Union[Model, int]]) -> list[int]:
    ids: set[int] = set()
    for obj in obs_or_ids:
        if isinstance(obj, int):
            ids.add(obj)
        else:
            ids.add(obj.pk)
    return list(ids)


def _update_queryset(queryset) -> int:
    return queryset.update(
        category=None,
        thread=None,
        post=None,
        uploader=None,
        is_deleted=True,
    )
