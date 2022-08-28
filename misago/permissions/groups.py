from collections import defaultdict
from typing import Iterable, List

from ..categories.models import Category, CategoryType
from ..context import Context
from ..users.models import UserGroup
from .permissions import CategoryPermission, CorePermission
from .queries import categories_permissions_query, permissions_query

GroupsPermissions = dict


async def get_groups_permissions(
    context: Context,
    groups: Iterable[UserGroup],
    *,
    anonymous: bool = False,
    moderated_categories: List[int] | None = None,
) -> GroupsPermissions:
    state: dict = {
        "groups": groups,
        "groups_ids": [group.id for group in groups],
        "categories": [],
        "moderated_categories": moderated_categories or [],
    }

    state["categories"] = (
        await Category.query.filter(type=CategoryType.THREADS).order_by("left").all()
    )

    groups_permissions: GroupsPermissions = {
        "core": set(),
        "category": {
            CategoryPermission.SEE: set(),
            CategoryPermission.READ: set(),
            CategoryPermission.START: set(),
            CategoryPermission.REPLY: set(),
            CategoryPermission.UPLOAD: set(),
            CategoryPermission.DOWNLOAD: set(),
            CategoryPermission.MODERATOR: set(),
        },
    }

    await get_groups_permissions_action(
        context,
        state,
        groups_permissions,
        anonymous=anonymous,
    )

    return groups_permissions


async def get_groups_permissions_action(
    context: Context,
    state: dict,
    groups_permissions: GroupsPermissions,
    *,
    anonymous: bool = False,
):
    for group in state["groups"]:
        if not anonymous:
            if group.is_admin:
                groups_permissions["core"].add(CorePermission.ADMIN)
            if group.is_moderator:
                groups_permissions["core"].add(CorePermission.MODERATOR)

    # Set core permissions
    core_perms = await permissions_query.filter(
        group_id__in=state["groups_ids"]
    ).all_flat("permission")
    groups_permissions["core"] = groups_permissions["core"].union(core_perms)

    # Get categories permissions
    categories_perms = defaultdict(set)
    categories_perms_query = await categories_permissions_query.filter(
        group_id__in=state["groups_ids"]
    ).all("category_id", "permission")

    # Merge categories permissions from all groups
    for category_id, permission in categories_perms_query:
        categories_perms[category_id].add(permission)

    # Set categories permissions
    for category in state["categories"]:
        # Skip categories with parent we can't read
        if (
            category.parent_id
            and category.parent_id
            not in groups_permissions["category"][CategoryPermission.READ]
        ):
            continue

        # Skip perms for invisible category
        if CategoryPermission.SEE not in categories_perms[category.id]:
            continue

        groups_permissions["category"][CategoryPermission.SEE].add(category.id)

        # Skip perms for unreadable category
        if CategoryPermission.READ not in categories_perms[category.id]:
            continue

        groups_permissions["category"][CategoryPermission.READ].add(category.id)

        # Set remaining permissions
        if not anonymous:
            # Only anonymous may publish content
            if CategoryPermission.START in categories_perms[category.id]:
                groups_permissions["category"][CategoryPermission.START].add(
                    category.id
                )

            if CategoryPermission.REPLY in categories_perms[category.id]:
                groups_permissions["category"][CategoryPermission.REPLY].add(
                    category.id
                )

            if CategoryPermission.UPLOAD in categories_perms[category.id]:
                groups_permissions["category"][CategoryPermission.UPLOAD].add(
                    category.id
                )

        if CategoryPermission.DOWNLOAD in categories_perms[category.id]:
            groups_permissions["category"][CategoryPermission.DOWNLOAD].add(category.id)
