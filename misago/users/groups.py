from django.contrib.auth import get_user_model
from django.http import HttpRequest

from ..permissions.models import CategoryGroupPermission, CategoryModerator
from ..postgres.delete import delete_all, delete_one
from ..postgres.execute import execute_fetch_all
from .hooks import delete_group_hook, set_default_group_hook
from .models import Group
from .tasks import remove_group_from_users_groups_ids

__all__ = [
    "count_groups_members",
    "delete_group",
    "set_default_group",
]

User = get_user_model()


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
    delete_all(CategoryModerator, group_id=group.id)
    delete_one(group)

    remove_group_from_users_groups_ids.delay(group.id)
