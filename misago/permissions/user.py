from typing import TYPE_CHECKING, Union

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache

from ..cache.enums import CacheName
from ..categories.enums import CategoryTree
from ..categories.models import Category
from ..users.enums import DefaultGroupId
from ..users.models import Group
from .enums import (
    CanHideOwnPostEdits,
    CanSeePostEdits,
    CanSeePostLikes,
    CanUploadAttachments,
    CategoryPermission,
)
from .hooks import (
    build_user_category_permissions_hook,
    build_user_permissions_hook,
    get_user_permissions_hook,
)
from .models import CategoryGroupPermission
from .operations import (
    if_greater,
    if_true,
    if_zero_or_greater,
)

if TYPE_CHECKING:
    from ..users.models import User


def get_user_permissions(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> dict:
    return get_user_permissions_hook(_get_user_permissions_action, user, cache_versions)


def _get_user_permissions_action(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> dict:
    cache_key = get_user_permissions_cache_key(user, cache_versions)
    permissions = cache.get(cache_key)

    if permissions is None:
        permissions = build_user_permissions(user)
        cache.set(cache_key, permissions)

    return permissions


def get_user_permissions_cache_key(
    user: Union["User", AnonymousUser], cache_versions: dict
) -> str:
    if user.is_anonymous:
        return f"anonymous:{cache_versions[CacheName.PERMISSIONS]}"

    return f"{user.permissions_id}:{cache_versions[CacheName.PERMISSIONS]}"


def build_user_permissions(user: Union["User", AnonymousUser]) -> dict:
    if user.is_anonymous:
        groups_ids = [DefaultGroupId.GUESTS]
    else:
        groups_ids = user.groups_ids

    groups: list[Group] = list(Group.objects.filter(id__in=groups_ids))
    permissions = build_user_permissions_hook(_build_user_permissions_action, groups)

    permissions["categories"] = build_user_category_permissions(groups, permissions)

    return permissions


def _build_user_permissions_action(groups: list[Group]) -> dict:
    permissions = {
        "can_use_private_threads": False,
        "can_start_private_threads": False,
        "private_thread_members_limit": 1,
        "can_edit_own_threads": False,
        "own_threads_edit_time_limit": 0,
        "can_edit_own_posts": False,
        "own_posts_edit_time_limit": 0,
        "can_see_others_post_edits": CanSeePostEdits.NEVER.value,
        "can_hide_own_post_edits": CanHideOwnPostEdits.NEVER.value,
        "own_post_edits_hide_time_limit": 0,
        "own_delete_post_edits_time_limit": 0,
        "exempt_from_flood_control": False,
        "can_upload_attachments": CanUploadAttachments.NEVER.value,
        "attachment_storage_limit": 0,
        "unused_attachments_storage_limit": 0,
        "attachment_size_limit": 0,
        "can_always_delete_own_attachments": False,
        "can_start_polls": False,
        "can_edit_own_polls": False,
        "own_polls_edit_time_limit": 0,
        "can_close_own_polls": False,
        "own_polls_close_time_limit": 0,
        "can_vote_in_polls": False,
        "can_like_posts": False,
        "can_see_own_post_likes": CanSeePostLikes.NEVER.value,
        "can_see_others_post_likes": CanSeePostLikes.NEVER.value,
        "can_change_username": False,
        "username_changes_limit": 0,
        "username_changes_expire": 0,
        "username_changes_span": 0,
        "can_see_user_profiles": False,
        "categories": {},
    }

    for group in groups:
        if_true(
            permissions,
            "can_use_private_threads",
            group.can_use_private_threads,
        )
        if_true(
            permissions,
            "can_start_private_threads",
            group.can_start_private_threads,
        )
        if_greater(
            permissions,
            "private_thread_members_limit",
            group.private_thread_members_limit,
        )
        if_true(
            permissions,
            "can_edit_own_threads",
            group.can_edit_own_threads,
        )
        if_zero_or_greater(
            permissions,
            "own_threads_edit_time_limit",
            group.own_threads_edit_time_limit,
        )
        if_true(
            permissions,
            "can_edit_own_posts",
            group.can_edit_own_posts,
        )
        if_zero_or_greater(
            permissions,
            "own_posts_edit_time_limit",
            group.own_posts_edit_time_limit,
        )
        if_greater(
            permissions,
            "can_see_others_post_edits",
            group.can_see_others_post_edits,
        )
        if_greater(
            permissions,
            "can_hide_own_post_edits",
            group.can_hide_own_post_edits,
        )
        if_zero_or_greater(
            permissions,
            "own_post_edits_hide_time_limit",
            group.own_post_edits_hide_time_limit,
        )
        if_zero_or_greater(
            permissions,
            "own_delete_post_edits_time_limit",
            group.own_delete_post_edits_time_limit,
        )
        if_true(
            permissions,
            "exempt_from_flood_control",
            group.exempt_from_flood_control,
        )
        if_greater(
            permissions,
            "can_upload_attachments",
            group.can_upload_attachments,
        )
        if_zero_or_greater(
            permissions,
            "attachment_storage_limit",
            group.attachment_storage_limit,
        )
        if_zero_or_greater(
            permissions,
            "unused_attachments_storage_limit",
            group.unused_attachments_storage_limit,
        )
        if_zero_or_greater(
            permissions,
            "attachment_size_limit",
            group.attachment_size_limit,
        )
        if_true(
            permissions,
            "can_always_delete_own_attachments",
            group.can_always_delete_own_attachments,
        )
        if_true(
            permissions,
            "can_start_polls",
            group.can_start_polls,
        )
        if_true(
            permissions,
            "can_edit_own_polls",
            group.can_edit_own_polls,
        )
        if_zero_or_greater(
            permissions,
            "own_polls_edit_time_limit",
            group.own_polls_edit_time_limit,
        )
        if_true(
            permissions,
            "can_close_own_polls",
            group.can_close_own_polls,
        )
        if_zero_or_greater(
            permissions,
            "own_polls_close_time_limit",
            group.own_polls_close_time_limit,
        )
        if_true(
            permissions,
            "can_like_posts",
            group.can_like_posts,
        )
        if_greater(
            permissions,
            "can_see_own_post_likes",
            group.can_see_own_post_likes,
        )
        if_greater(
            permissions,
            "can_see_others_post_likes",
            group.can_see_others_post_likes,
        )
        if_true(
            permissions,
            "can_vote_in_polls",
            group.can_vote_in_polls,
        )
        if_true(
            permissions,
            "can_change_username",
            group.can_change_username,
        )
        if_zero_or_greater(
            permissions,
            "username_changes_limit",
            group.username_changes_limit,
        )
        if_zero_or_greater(
            permissions,
            "username_changes_expire",
            group.username_changes_expire,
        )
        if_zero_or_greater(
            permissions,
            "username_changes_span",
            group.username_changes_span,
        )
        if_true(
            permissions,
            "can_see_user_profiles",
            group.can_see_user_profiles,
        )

    return permissions


def build_user_category_permissions(groups: list[Group], permissions: dict) -> dict:
    categories: dict[int, Category] = {
        category.id: category
        for category in Category.objects.filter(
            tree_id=CategoryTree.THREADS,
            level__gt=0,
        )
    }

    category_permissions_queryset = CategoryGroupPermission.objects.filter(
        group__in=groups,
        category__in=categories.values(),
    ).values_list("category_id", "permission")

    category_permissions: dict[int, list[str]] = {}
    for category_id, permission in category_permissions_queryset:
        if category_id not in category_permissions:
            category_permissions[category_id] = []

        if permission not in category_permissions[category_id]:
            category_permissions[category_id].append(permission)

    return build_user_category_permissions_hook(
        _build_user_category_permissions_action,
        groups,
        categories,
        category_permissions,
        permissions,
    )


def _build_user_category_permissions_action(
    groups: list[Group],
    categories: dict[int, Category],
    category_permissions: dict[int, list[str]],
    user_permissions: dict,
) -> dict:
    permissions = {
        CategoryPermission.SEE: [],
        CategoryPermission.BROWSE: [],
        CategoryPermission.START: [],
        CategoryPermission.REPLY: [],
        CategoryPermission.ATTACHMENTS: [],
    }

    for category_id, category in categories.items():
        # Skip category if we can't see its parent
        if not can_see_parent_category(category, categories, permissions):
            continue

        # Skip category if we can't see it
        perms = category_permissions.get(category_id, [])
        if CategoryPermission.SEE not in perms:
            continue

        permissions[CategoryPermission.SEE].append(category_id)

        if CategoryPermission.BROWSE in perms:
            permissions[CategoryPermission.BROWSE].append(category_id)
        else:
            continue  # Skip rest of permissions if we can't read its contents

        if CategoryPermission.START in perms:
            permissions[CategoryPermission.START].append(category_id)
        if CategoryPermission.REPLY in perms:
            permissions[CategoryPermission.REPLY].append(category_id)
        if CategoryPermission.ATTACHMENTS in perms:
            permissions[CategoryPermission.ATTACHMENTS].append(category_id)

    return permissions


def can_see_parent_category(
    category: Category,
    categories: dict[int, Category],
    permissions: dict,
) -> bool:
    if category.level <= 1:
        return True

    if category.parent_id in permissions[CategoryPermission.BROWSE]:
        return True

    if category.parent_id in permissions[CategoryPermission.SEE]:
        return categories[category.parent_id].delay_browse_check

    return False
