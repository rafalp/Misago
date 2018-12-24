"""
Service for tracking namechanges
"""
from datetime import timedelta

from django.utils import timezone


def get_username_options(settings, user, user_acl):
    changes_left = get_left_namechanges(user, user_acl)
    next_on = get_next_available_namechange(user, user_acl, changes_left)

    return {
        "changes_left": changes_left,
        "next_on": next_on,
        "length_min": settings.username_length_min,
        "length_max": settings.username_length_max,
    }


def get_left_namechanges(user, user_acl):
    name_changes_allowed = user_acl["name_changes_allowed"]
    if not name_changes_allowed:
        return 0

    valid_changes = get_valid_changes_queryset(user, user_acl)
    used_changes = valid_changes.count()
    if name_changes_allowed <= used_changes:
        return 0
    return name_changes_allowed - used_changes


def get_next_available_namechange(user, user_acl, changes_left):
    name_changes_expire = user_acl["name_changes_expire"]
    if changes_left or not name_changes_expire:
        return None

    valid_changes = get_valid_changes_queryset(user, user_acl)
    name_last_changed_on = valid_changes.latest().changed_on
    return name_last_changed_on + timedelta(days=name_changes_expire)


def get_valid_changes_queryset(user, user_acl):
    name_changes_expire = user_acl["name_changes_expire"]
    queryset = user.namechanges.filter(changed_by=user)
    if user_acl["name_changes_expire"]:
        cutoff = timezone.now() - timedelta(days=name_changes_expire)
        return queryset.filter(changed_on__gte=cutoff)
    return queryset
