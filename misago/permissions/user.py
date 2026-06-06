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
    PermissionValue,
)
from .hooks import (
    build_user_category_permissions_hook,
    build_user_permissions_hook,
    get_user_permissions_hook,
)
from .models import CategoryGroupPermission
from .rules import yes_no_never, zero_or_greater

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


if_true = lambda x: bool(max())

PERMISSION_RULES = {
    "can_use_private_threads": yes_no_never,
    "can_start_private_threads": yes_no_never,
    "private_thread_members_limit": max,
    "can_edit_own_threads": yes_no_never,
    "own_threads_edit_time_limit": zero_or_greater,
    "can_edit_own_posts": yes_no_never,
    "own_posts_edit_time_limit": zero_or_greater,
    "can_see_others_post_edits": max,
    "can_hide_own_post_edits": max,
    "own_post_edits_hide_time_limit": zero_or_greater,
    "own_delete_post_edits_time_limit": zero_or_greater,
    "bypass_flood_control": any,
    "bypass_content_approval": any,
    "can_upload_attachments": max,
    "attachment_storage_limit": zero_or_greater,
    "unused_attachments_storage_limit": zero_or_greater,
    "attachment_size_limit": zero_or_greater,
    "can_always_delete_own_attachments": any,
    "can_start_polls": any,
    "can_edit_own_polls": any,
    "own_polls_edit_time_limit": zero_or_greater,
    "can_close_own_polls": any,
    "own_polls_close_time_limit": zero_or_greater,
    "can_vote_in_polls": any,
    "can_like_posts": any,
    "can_see_own_post_likes": max,
    "can_see_others_post_likes": max,
    "can_select_own_thread_solutions": any,
    "can_change_own_thread_solutions": any,
    "own_thread_solutions_change_time_limit": zero_or_greater,
    "can_clear_own_thread_solutions": any,
    "own_thread_solutions_clear_time_limit": zero_or_greater,
    "can_change_username": any,
    "username_changes_limit": zero_or_greater,
    "username_changes_expire": zero_or_greater,
    "username_changes_span": zero_or_greater,
    "can_see_user_profiles": any,
}

PERMISSION_DEFAULTS = {
    "private_thread_members_limit": 1,
    "own_threads_edit_time_limit": 0,
    "own_posts_edit_time_limit": 0,
    "own_post_edits_hide_time_limit": 0,
    "own_delete_post_edits_time_limit": 0,
    "attachment_storage_limit": 0,
    "unused_attachments_storage_limit": 0,
    "attachment_size_limit": 0,
    "own_polls_edit_time_limit": 0,
    "own_polls_close_time_limit": 0,
    "own_thread_solutions_change_time_limit": 0,
    "own_thread_solutions_clear_time_limit": 0,
    "username_changes_limit": 0,
    "username_changes_expire": 0,
    "username_changes_span": 0,
}


def _build_user_permissions_action(groups: list[Group]) -> dict:
    groups_permissions = {
        "can_use_private_threads": set(),
        "can_start_private_threads": set(),
        "private_thread_members_limit": {1},
        "can_edit_own_threads": set(),
        "own_threads_edit_time_limit": set(),
        "can_edit_own_posts": set(),
        "own_posts_edit_time_limit": set(),
        "can_see_others_post_edits": set(),
        "can_hide_own_post_edits": set(),
        "own_post_edits_hide_time_limit": set(),
        "own_delete_post_edits_time_limit": set(),
        "bypass_flood_control": set(),
        "bypass_content_approval": set(),
        "can_upload_attachments": set(),
        "attachment_storage_limit": set(),
        "unused_attachments_storage_limit": set(),
        "attachment_size_limit": set(),
        "can_always_delete_own_attachments": set(),
        "can_start_polls": set(),
        "can_edit_own_polls": set(),
        "own_polls_edit_time_limit": set(),
        "can_close_own_polls": set(),
        "own_polls_close_time_limit": set(),
        "can_vote_in_polls": set(),
        "can_like_posts": set(),
        "can_see_own_post_likes": set(),
        "can_see_others_post_likes": set(),
        "can_select_own_thread_solutions": set(),
        "can_change_own_thread_solutions": set(),
        "own_thread_solutions_change_time_limit": set(),
        "can_clear_own_thread_solutions": set(),
        "own_thread_solutions_clear_time_limit": set(),
        "can_change_username": set(),
        "username_changes_limit": set(),
        "username_changes_expire": set(),
        "username_changes_span": set(),
        "can_see_user_profiles": set(),
    }

    for group in groups:
        groups_permissions["can_use_private_threads"].add(group.can_use_private_threads)
        groups_permissions["can_start_private_threads"].add(
            group.can_start_private_threads
        )
        groups_permissions["private_thread_members_limit"].add(
            group.private_thread_members_limit
        )
        groups_permissions["can_edit_own_threads"].add(group.can_edit_own_threads)
        if group.can_edit_own_threads == PermissionValue.YES:
            groups_permissions["own_threads_edit_time_limit"].add(
                group.own_threads_edit_time_limit
            )
        groups_permissions["can_edit_own_posts"].add(group.can_edit_own_posts)
        if group.can_edit_own_posts == PermissionValue.YES:
            groups_permissions["own_posts_edit_time_limit"].add(
                group.own_posts_edit_time_limit
            )
        groups_permissions["can_see_others_post_edits"].add(
            group.can_see_others_post_edits
        )
        groups_permissions["can_hide_own_post_edits"].add(group.can_hide_own_post_edits)
        if group.can_hide_own_post_edits >= CanHideOwnPostEdits.HIDE:
            groups_permissions["own_post_edits_hide_time_limit"].add(
                group.own_post_edits_hide_time_limit
            )
        if group.can_hide_own_post_edits == CanHideOwnPostEdits.DELETE:
            groups_permissions["own_delete_post_edits_time_limit"].add(
                group.own_delete_post_edits_time_limit
            )
        groups_permissions["bypass_flood_control"].add(group.bypass_flood_control)
        groups_permissions["bypass_content_approval"].add(group.bypass_content_approval)
        groups_permissions["can_upload_attachments"].add(group.can_upload_attachments)
        if group.can_upload_attachments:
            groups_permissions["attachment_storage_limit"].add(
                group.attachment_storage_limit
            )
            groups_permissions["unused_attachments_storage_limit"].add(
                group.unused_attachments_storage_limit
            )
            groups_permissions["attachment_size_limit"].add(group.attachment_size_limit)
        groups_permissions["can_always_delete_own_attachments"].add(
            group.can_always_delete_own_attachments
        )
        groups_permissions["can_start_polls"].add(group.can_start_polls)
        groups_permissions["can_edit_own_polls"].add(group.can_edit_own_polls)
        if group.can_edit_own_polls:
            groups_permissions["own_polls_edit_time_limit"].add(
                group.own_polls_edit_time_limit
            )
        groups_permissions["can_close_own_polls"].add(group.can_close_own_polls)
        if group.can_close_own_polls:
            groups_permissions["own_polls_close_time_limit"].add(
                group.own_polls_close_time_limit
            )
        groups_permissions["can_vote_in_polls"].add(group.can_vote_in_polls)
        groups_permissions["can_like_posts"].add(group.can_like_posts)
        groups_permissions["can_see_own_post_likes"].add(group.can_see_own_post_likes)
        groups_permissions["can_see_others_post_likes"].add(
            group.can_see_others_post_likes
        )
        groups_permissions["can_select_own_thread_solutions"].add(
            group.can_select_own_thread_solutions
        )
        groups_permissions["can_change_own_thread_solutions"].add(
            group.can_change_own_thread_solutions
        )
        if group.can_change_own_thread_solutions:
            groups_permissions["own_thread_solutions_change_time_limit"].add(
                group.own_thread_solutions_change_time_limit
            )
        groups_permissions["can_clear_own_thread_solutions"].add(
            group.can_clear_own_thread_solutions
        )
        if group.can_clear_own_thread_solutions:
            groups_permissions["own_thread_solutions_clear_time_limit"].add(
                group.own_thread_solutions_clear_time_limit
            )
        groups_permissions["can_change_username"].add(group.can_change_username)
        if group.can_change_username:
            groups_permissions["username_changes_limit"].add(
                group.username_changes_limit
            )
            groups_permissions["username_changes_expire"].add(
                group.username_changes_expire
            )
            groups_permissions["username_changes_span"].add(group.username_changes_span)
        groups_permissions["can_see_user_profiles"].add(group.can_see_user_profiles)

    permissions = {
        "categories": {},
    }

    for permission, rule in PERMISSION_RULES.items():
        if groups_permissions[permission]:
            permissions[permission] = rule(groups_permissions[permission])
        else:
            permissions[permission] = PERMISSION_DEFAULTS[permission]

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
