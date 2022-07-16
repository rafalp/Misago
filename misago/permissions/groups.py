from collections import defaultdict
from typing import Iterable, List

from ..categories.models import Category, CategoryType
from ..users.models import UserGroup
from .permissions import CategoryPermission, CorePermission
from .queries import categories_permissions_query, permissions_query

GroupsPermissions = dict


async def get_groups_permissions(groups: Iterable[UserGroup]) -> GroupsPermissions:
    state: dict = {
        "groups": groups,
        "groups_ids": [group.id for group in groups],
        "categories": [],
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
        },
    }

    await get_groups_permissions_action(state, groups_permissions)

    return groups_permissions


async def get_groups_permissions_action(
    state: dict, groups_permissions: GroupsPermissions
):
    for group in state["groups"]:
        if group.is_admin:
            append_unique(groups_permissions["core"], CorePermission.ADMIN)
        if group.is_moderator:
            append_unique(groups_permissions["core"], CorePermission.MODERATOR)

    core_perms = await permissions_query.filter(group_id__in=state["groups_ids"]).all(
        "permission", flat=True
    )
    groups_permissions["core"] = list(
        sorted(set(groups_permissions["core"] + core_perms))
    )

    categories_perms = defaultdict(set)
    categories_perms_query = await categories_permissions_query.filter(
        group_id__in=state["groups_ids"]
    ).all("category_id", "permission")
    for row in categories_perms_query:
        categories_perms[row["category_id"]].add(row["permission"])

    for category in state["categories"]:
        # Skip categories with parent we can't read
        if category.parent_id and category.parent_id not in groups_permissions["category"][CategoryPermission.READ]:
            continue

        # Skip perms for invisible category
        if CategoryPermission.SEE not in categories_perms[category.id]:
            continue

        append_unique(
            groups_permissions["category"][CategoryPermission.SEE],
            category.id,
        )

        # Skip perms for unreadable category
        if CategoryPermission.READ not in categories_perms[category.id]:
            continue

        append_unique(
            groups_permissions["category"][CategoryPermission.READ],
            category.id,
        )

        # Set remaining permissions
        if CategoryPermission.START in categories_perms[category.id]:
            append_unique(
                groups_permissions["category"][CategoryPermission.START],
                category.id,
            )

        if CategoryPermission.REPLY in categories_perms[category.id]:
            append_unique(
                groups_permissions["category"][CategoryPermission.REPLY],
                category.id,
            )

        if CategoryPermission.UPLOAD in categories_perms[category.id]:
            append_unique(
                groups_permissions["category"][CategoryPermission.UPLOAD],
                category.id,
            )

        if CategoryPermission.DOWNLOAD in categories_perms[category.id]:
            append_unique(
                groups_permissions["category"][CategoryPermission.DOWNLOAD],
                category.id,
            )



def append_unique(list_: List[int], value: int):
    if value not in list_:
        list_.append(value)
