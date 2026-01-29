from typing import Type

from django.db.models import Model
from django.http import HttpRequest

from ..attachments.delete import delete_categories_attachments
from ..attachments.models import Attachment
from ..categories.models import RoleCategoryACL
from ..edits.models import PostEdit
from ..likes.models import Like
from ..notifications.models import Notification, WatchedThread
from ..permissions.models import CategoryGroupPermission
from ..polls.models import Poll, PollVote
from ..postgres.delete import delete_all
from ..readtracker.models import ReadCategory, ReadThread
from ..threads.models import (
    Attachment as LegacyAttachment,
    Post,
    Thread,
)
from ..threadupdates.models import ThreadUpdate
from .hooks import delete_categories_hook
from .models import Category

__all__ = ["delete_category"]


def delete_category(
    category: Category,
    *,
    move_children_to: Category | bool | None = True,
    move_contents_to: Category | None = None,
    request: HttpRequest | None = None,
):
    if isinstance(move_children_to, Category) and move_children_to.is_descendant_of(
        category, include_self=True
    ):
        raise ValueError("Category from 'move_children_to' will be deleted.")

    if move_contents_to and (
        move_contents_to == category
        or (
            move_children_to is None
            and move_contents_to.is_descendant_of(category, include_self=True)
        )
    ):
        raise ValueError("Category from 'move_contents_to' will be deleted.")

    categories: list[Category] = [category]
    if move_children_to is None:
        categories = list(category.get_descendants(include_self=True))

    delete_categories_hook(
        _delete_categories_action,
        categories,
        move_children_to=move_children_to,
        move_contents_to=move_contents_to,
        request=request,
    )


def _delete_categories_action(
    categories: list[Category],
    *,
    move_contents_to: Category | None = None,
    move_children_to: Category | bool | None = True,
    request: HttpRequest | None = None,
):
    delete_all(RoleCategoryACL, category_id=categories)
    delete_all(CategoryGroupPermission, category_id=categories)
    delete_all(ReadCategory, category_id=categories)

    ThreadUpdate.objects.filter(
        context_type="misago_categories.category",
        context_id__in=[c.id for c in categories],
    ).clear_context_objects()

    Category.objects.filter(archive_pruned_in__in=categories).update(
        archive_pruned_in=None, last_thread=None
    )

    if move_contents_to:
        _move_categories_contents(categories, move_contents_to)
    else:
        _delete_categories_contents(request, categories)

    if move_children_to is True:
        for child in categories[0].get_children():
            root_category = Category.objects.root_category()
            child.refresh_from_db()
            child.move_to(root_category, position="last-child")
    elif move_children_to:
        for child in categories[0].get_children():
            move_children_to.refresh_from_db()
            child.refresh_from_db()
            child.move_to(move_children_to, position="last-child")

    for category in sorted(categories, key=lambda c: c.lft, reverse=True):
        category.delete()


def _move_categories_contents(categories: list[Category], new_category: Category):
    # misago.attachments
    _move_objects(Attachment, categories, new_category)

    # misago.edits
    _move_objects(PostEdit, categories, new_category)

    # misago.likes
    _move_objects(Like, categories, new_category)

    # misago.notifications
    _move_objects(Notification, categories, new_category)
    _move_objects(WatchedThread, categories, new_category)

    # misago.polls
    _move_objects(Poll, categories, new_category)
    _move_objects(PollVote, categories, new_category)

    # misago.readtracker
    _move_objects(ReadThread, categories, new_category)

    # misago.threads
    _move_objects(Post, categories, new_category)
    _move_objects(Thread, categories, new_category)

    # misago.threadupdates
    _move_objects(ThreadUpdate, categories, new_category)

    new_category.synchronize()
    new_category.save()


def _move_objects(
    model: Type[Model], categories: list[Category], new_category: Category
):
    model.objects.filter(category__in=categories).update(category=new_category)


def _delete_categories_contents(
    request: HttpRequest | None, categories: list[Category]
):
    delete_categories_attachments(categories, request=request)

    delete_all(Notification, category_id=categories)
    delete_all(WatchedThread, category_id=categories)

    LegacyAttachment.objects.filter(post__category__in=categories).update(post=None)

    Thread.objects.filter(post__category__in=categories).update(
        first_post=None, last_post=None
    )

    delete_all(Like, category_id=categories)
    delete_all(PollVote, category_id=categories)
    delete_all(Poll, category_id=categories)
    delete_all(PostEdit, category_id=categories)
    delete_all(Post, category_id=categories)
    delete_all(ThreadUpdate, category_id=categories)
    delete_all(Thread, category_id=categories)
