import pytest
from django.core.exceptions import PermissionDenied

from ...threads.models import ThreadParticipant
from ...threads.test import post_thread
from ..privatethreads import (
    check_private_threads_permission,
    check_start_private_threads_permission,
    filter_private_threads_queryset,
)
from ..proxy import UserPermissionsProxy


def test_check_private_threads_permission_passes_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_has_no_permission(
    user, members_group, cache_versions
):
    members_group.can_use_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)


def test_check_private_threads_permission_fails_if_user_is_anonymous(
    anonymous_user, cache_versions
):
    permissions = UserPermissionsProxy(anonymous_user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_private_threads_permission(permissions)


def test_check_start_private_threads_permission_passes_if_user_has_permission(
    user, cache_versions
):
    permissions = UserPermissionsProxy(user, cache_versions)
    check_start_private_threads_permission(permissions)


def test_check_start_private_threads_permission_fails_if_user_has_no_permission(
    user, members_group, cache_versions
):
    members_group.can_start_private_threads = False
    members_group.save()

    permissions = UserPermissionsProxy(user, cache_versions)

    with pytest.raises(PermissionDenied):
        check_start_private_threads_permission(permissions)


def test_filter_private_threads_queryset_returns_nothing_for_anonymous_user(
    private_threads_category, anonymous_user, cache_versions
):
    post_thread(private_threads_category)

    permissions = UserPermissionsProxy(anonymous_user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert not queryset.exists()


def test_filter_private_threads_queryset_returns_thread_for_user_who_is_a_thread_participant(
    private_threads_category, user, cache_versions
):
    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(thread=thread, user=user)

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert thread in list(queryset)


def test_filter_private_threads_queryset_excludes_thread_user_is_not_participating_in(
    private_threads_category, user, other_user, cache_versions
):
    thread = post_thread(private_threads_category)
    ThreadParticipant.objects.create(thread=thread, user=other_user)

    permissions = UserPermissionsProxy(user, cache_versions)
    queryset = filter_private_threads_queryset(
        permissions, private_threads_category.thread_set
    )
    assert not queryset.exists()
