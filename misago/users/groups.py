from django.contrib.auth import get_user_model
from django.http import HttpRequest

from ..core.utils import slugify
from ..permissions.models import CategoryGroupPermission, Moderator
from ..postgres.delete import delete_all, delete_one
from ..postgres.execute import execute_fetch_all
from .hooks import (
    create_group_hook,
    delete_group_hook,
    set_default_group_hook,
    update_group_hook,
    update_group_description_hook,
)
from .models import Group, GroupDescription
from .tasks import remove_group_from_users_groups_ids

__all__ = [
    "count_groups_members",
    "create_group",
    "delete_group",
    "set_default_group",
]

User = get_user_model()


def create_group(**kwargs) -> Group:
    if not kwargs.get("name"):
        raise ValueError("The 'name' named argument is required.")

    kwargs.setdefault("request", None)
    kwargs.setdefault("form", None)
    kwargs.setdefault("plugin_data", {})

    return create_group_hook(_create_group_action, **kwargs)


def _create_group_action(**kwargs) -> Group:
    ordering = (
        Group.objects.order_by("-ordering").values_list("ordering", flat=True).first()
    )
    kwargs["ordering"] = ordering + 1

    if not kwargs.get("slug"):
        kwargs["slug"] = slugify(kwargs["name"])

    if "request" in kwargs:
        kwargs.pop("request")
    if "form" in kwargs:
        kwargs.pop("form")

    group = Group.objects.create(**kwargs)
    group.description = GroupDescription.objects.create(group=group)

    return group


def update_group(group: Group, **kwargs) -> Group:
    kwargs.setdefault("request", None)
    kwargs.setdefault("form", None)
    return update_group_hook(_update_group_action, group, **kwargs)


GROUP_FIELDS = tuple(field.name for field in Group._meta.get_fields())


def _update_group_action(group: Group, **kwargs) -> Group:
    if "request" in kwargs:
        kwargs.pop("request")
    if "form" in kwargs:
        kwargs.pop("form")

    if "slug" in kwargs and not kwargs["slug"]:
        if kwargs.get("name"):
            kwargs["slug"] = slugify(kwargs["name"])
        else:
            kwargs["slug"] = slugify(group.name)
    elif kwargs.get("name") and not kwargs.get("slug"):
        kwargs["slug"] = slugify(kwargs["name"])

    for attr_name, value in kwargs.items():
        if attr_name not in GROUP_FIELDS:
            raise TypeError(f"cannot set '{attr_name}' attribute on 'Group'")

        setattr(group, attr_name, None if value == "" else value)

    group.save()
    return group


GROUP_DESCRIPTION_FIELDS = tuple(
    field.name for field in GroupDescription._meta.get_fields()
)


def update_group_description(group: Group, **kwargs) -> Group:
    kwargs.setdefault("request", None)
    kwargs.setdefault("form", None)
    return update_group_description_hook(
        _update_group_description_action, group, **kwargs
    )


def _update_group_description_action(group: Group, **kwargs) -> Group:
    if "request" in kwargs:
        kwargs.pop("request")
    if "form" in kwargs:
        kwargs.pop("form")

    for attr_name, value in kwargs.items():
        if attr_name not in GROUP_DESCRIPTION_FIELDS:
            raise TypeError(f"cannot set '{attr_name}' attribute on 'GroupDescription'")

        setattr(group.description, attr_name, None if value == "" else value)

    group.description.save()
    return group


def count_groups_members() -> list[tuple[int, int]]:
    """Returns a list of (group id, members count) tuples.

    Excludes groups without any members from results.
    """

    user_table = User._meta.db_table
    result = execute_fetch_all(
        f'SELECT UNNEST("groups_ids") AS "gid", COUNT(*) FROM "{user_table}" GROUP BY "gid";'
    )
    return list(map(tuple, result))


def set_default_group(group: Group, request: HttpRequest | None = None):
    """Sets group as default"""
    set_default_group_hook(_set_default_group_action, group, HttpRequest)


def _set_default_group_action(group: Group, request: HttpRequest | None = None):
    Group.objects.filter(id=group.id).update(is_default=True)
    Group.objects.exclude(id=group.id).update(is_default=False)


def delete_group(group: Group, request: HttpRequest | None = None):
    """Deletes group with its relations from the database, bypassing the Django ORM."""
    delete_group_hook(_delete_group_action, group, request)


def _delete_group_action(group: Group, request: HttpRequest | None = None):
    delete_all(CategoryGroupPermission, group_id=group.id)
    delete_all(Moderator, group_id=group.id)
    delete_all(GroupDescription, group_id=group.id)
    delete_one(group)

    remove_group_from_users_groups_ids.delay(group.id)
