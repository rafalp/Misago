from collections import defaultdict
from typing import Iterable, List

from ..categories.models import Category, CategoryType
from ..context import Context
from ..users.models import UserGroup
from .permissions import CategoryPermission, CorePermission
from .queries import categories_permissions_query, permissions_query
from .utils import add_permission

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
        "core": [],
        "category": {
            CategoryPermission.SEE: [],
            CategoryPermission.READ: [],
            CategoryPermission.START: [],
            CategoryPermission.REPLY: [],
            CategoryPermission.UPLOAD: [],
            CategoryPermission.DOWNLOAD: [],
            CategoryPermission.MODERATOR: [],
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
                add_permission(groups_permissions["core"], CorePermission.ADMIN)
            if group.is_moderator:
                add_permission(groups_permissions["core"], CorePermission.MODERATOR)

    # Set core permissions
    core_perms = await permissions_query.filter(
        group_id__in=state["groups_ids"]
    ).all_flat("permission")
    groups_permissions["core"] = list(
        sorted(set(groups_permissions["core"] + core_perms))
    )

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

        add_permission(
            groups_permissions["category"][CategoryPermission.SEE],
            category.id,
        )

        # Skip perms for unreadable category
        if CategoryPermission.READ not in categories_perms[category.id]:
            continue

        add_permission(
            groups_permissions["category"][CategoryPermission.READ],
            category.id,
        )

        # Set remaining permissions
        if not anonymous:
            # Only anonymous may publish content
            if CategoryPermission.START in categories_perms[category.id]:
                add_permission(
                    groups_permissions["category"][CategoryPermission.START],
                    category.id,
                )

            if CategoryPermission.REPLY in categories_perms[category.id]:
                add_permission(
                    groups_permissions["category"][CategoryPermission.REPLY],
                    category.id,
                )

            if CategoryPermission.UPLOAD in categories_perms[category.id]:
                add_permission(
                    groups_permissions["category"][CategoryPermission.UPLOAD],
                    category.id,
                )

            if category.id in state["moderated_categories"]:
                for permission in CategoryPermission:
                    add_permission(
                        permission,
                        category.id,
                    )

        if CategoryPermission.DOWNLOAD in categories_perms[category.id]:
            add_permission(
                groups_permissions["category"][CategoryPermission.DOWNLOAD],
                category.id,
            )
