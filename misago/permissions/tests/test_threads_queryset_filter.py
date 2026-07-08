from itertools import product

import pytest

from ...categories.proxy import CategoriesProxy
from ...threads.enums import ThreadPinned
from ...threads.models import Thread
from ..proxy import UserPermissionsProxy
from ..threads import filter_threads_queryset


def test_threads_queryset_includes_category_with_see_and_browse_permission(
    threads_filter_factory,
    category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset


def test_threads_queryset_includes_category_with_see_permission_and_delay_browse(
    threads_filter_factory,
    category,
    category_thread,
    category_members_see_permission,
    user,
):
    category.delay_browse_check = True
    category.save()

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset


def test_threads_queryset_excludes_category_without_any_permissions(
    threads_filter_factory,
    category_thread,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert not queryset.exists()


def test_threads_queryset_excludes_category_with_only_see_permission(
    threads_filter_factory,
    category_thread,
    category_members_see_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert not queryset.exists()


def test_threads_queryset_combines_multiple_categories_with_see_and_browse_permission(
    threads_filter_factory,
    category_thread,
    child_category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset
    assert child_category_thread in queryset


@pytest.mark.slow
def test_threads_queryset_filter(
    thread_factory,
    threads_filter_factory,
    category,
    child_category,
    moderator,
    category_moderator,
    anonymous_user,
    user,
    other_user,
    category_guests_see_permission,
    category_guests_browse_permission,
    category_members_see_permission,
    category_members_browse_permission,
    category_moderators_see_permission,
    category_moderators_browse_permission,
    child_category_guests_see_permission,
    child_category_guests_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    child_category_moderators_see_permission,
    child_category_moderators_browse_permission,
):
    MATRIX = (
        (moderator, category_moderator, anonymous_user, user, other_user),
        (category, child_category),
        (False, True),
        (anonymous_user, user, other_user),
        (ThreadPinned.NONE, ThreadPinned.CATEGORY, ThreadPinned.EVERYWHERE),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_threads_queryset_filter_case(
            thread_factory, threads_filter_factory, *args
        )


def check_threads_queryset_filter_case(
    thread_factory,
    threads_filter_factory,
    user,
    category,
    started_only,
    starter,
    thread_pinned,
    thread_unapproved,
    thread_hidden,
):
    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = thread_factory(
        category,
        starter=starter if starter.is_authenticated else "Anon",
        pinned=thread_pinned,
        is_unapproved=thread_unapproved,
        is_hidden=thread_hidden,
    )

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    if thread in queryset:
        assert_queryset_contains(user, category, thread)
    else:
        assert_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_queryset_contains(user, category, thread):
    if thread.pinned == ThreadPinned.EVERYWHERE:
        raise AssertionError(f"queryset result contains a thread pinned everywhere")

    if user.id and (user.slug == "moderator" or user.slug == "categorymoderator"):
        return

    if thread.is_hidden:
        raise AssertionError(
            "queryset result for a user without moderator permissions contains "
            "a hidden thread"
        )

    if user.is_anonymous and thread.is_unapproved:
        raise AssertionError(
            "queryset result for an anonymous user contains an unapproved thread"
        )

    if (
        user.is_anonymous
        and category.show_started_only
        and thread.pinned != ThreadPinned.CATEGORY
    ):
        raise AssertionError(
            "queryset result for an anonymous user and category with "
            "show_started_only=true contains a thread that's not pinned in category"
        )

    if user.is_authenticated and thread.is_unapproved and thread.starter_id != user.id:
        raise AssertionError(
            "queryset result for a user without moderator permissions contains "
            "an unapproved thread started by a different user"
        )

    if (
        user.is_authenticated
        and category.show_started_only
        and not thread.pinned
        and thread.starter_id != user.id
    ):
        raise AssertionError(
            "queryset result for a category with show_started_only=true "
            "contains not pinned thread that's not started by the user"
        )


def assert_queryset_not_contains(user, category, thread):
    if thread.pinned == ThreadPinned.EVERYWHERE:
        return

    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        raise AssertionError("queryset result for a moderator is missing a thread")

    if thread.is_hidden:
        return

    if user.is_anonymous and thread.is_unapproved:
        return

    if user.is_authenticated and thread.is_unapproved and thread.starter_id == user.id:
        raise AssertionError(
            "queryset result for a user without moderator permissions is missing "
            "an unapproved thread started by them"
        )

    if (
        user.is_authenticated
        and category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "queryset result for a user is missing a thread started by them"
        )


def test_threads_pinned_queryset_includes_category_with_see_and_browse_permission(
    threads_filter_factory,
    category_pinned_everywhere_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_everywhere_thread in queryset


def test_threads_pinned_queryset_includes_category_with_see_permission_and_delay_browse(
    threads_filter_factory,
    category,
    category_pinned_everywhere_thread,
    category_members_see_permission,
    user,
):
    category.delay_browse_check = True
    category.save()

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_everywhere_thread in queryset


def test_threads_pinned_queryset_excludes_category_without_any_permissions(
    threads_filter_factory,
    category_pinned_everywhere_thread,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert not queryset.exists()


def test_threads_pinned_queryset_excludes_category_with_only_see_permission(
    threads_filter_factory,
    category_pinned_everywhere_thread,
    category_members_see_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert not queryset.exists()


def test_threads_pinned_queryset_combines_multiple_categories_with_see_and_browse_permission(
    threads_filter_factory,
    category_pinned_everywhere_thread,
    child_category_pinned_everywhere_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_everywhere_thread in queryset
    assert child_category_pinned_everywhere_thread in queryset


@pytest.mark.slow
def test_threads_queryset_filter_pinned(
    thread_factory,
    threads_filter_factory,
    category,
    child_category,
    moderator,
    category_moderator,
    anonymous_user,
    user,
    other_user,
    category_guests_see_permission,
    category_guests_browse_permission,
    category_members_see_permission,
    category_members_browse_permission,
    category_moderators_see_permission,
    category_moderators_browse_permission,
    child_category_guests_see_permission,
    child_category_guests_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    child_category_moderators_see_permission,
    child_category_moderators_browse_permission,
):
    MATRIX = (
        (moderator, category_moderator, anonymous_user, user, other_user),
        (category, child_category),
        (False, True),
        (anonymous_user, user, other_user),
        (ThreadPinned.NONE, ThreadPinned.CATEGORY, ThreadPinned.EVERYWHERE),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_threads_queryset_filter_pinned_case(
            thread_factory, threads_filter_factory, *args
        )


def check_threads_queryset_filter_pinned_case(
    thread_factory,
    threads_filter_factory,
    user,
    category,
    started_only,
    starter,
    thread_pinned,
    thread_unapproved,
    thread_hidden,
):
    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = thread_factory(
        category,
        starter=starter if starter.is_authenticated else "Anon",
        pinned=thread_pinned,
        is_unapproved=thread_unapproved,
        is_hidden=thread_hidden,
    )

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    if thread in queryset:
        assert_pinned_queryset_contains(user, category, thread)
    else:
        assert_pinned_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_pinned_queryset_contains(user, category, thread):
    if thread.pinned != ThreadPinned.EVERYWHERE:
        raise AssertionError(
            "pinned queryset result contains a thread that's not pinned everywhere"
        )

    if user.id and (user.slug == "moderator" or user.slug == "categorymoderator"):
        return

    if thread.is_hidden:
        raise AssertionError(
            "pinned queryset result for a user without moderator permissions "
            "contains a hidden thread"
        )

    if user.is_anonymous and thread.is_unapproved:
        raise AssertionError(
            "pinned queryset result for an anonymous user contains an unapproved thread"
        )

    if user.is_authenticated and thread.is_unapproved and thread.starter_id != user.id:
        raise AssertionError(
            "queryset result for a user without moderator permissions contains "
            "an unapproved thread started by a different user"
        )


def assert_pinned_queryset_not_contains(user, category, thread):
    if thread.pinned != ThreadPinned.EVERYWHERE:
        return

    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        raise AssertionError("queryset result for a moderator is missing a thread")

    if thread.is_hidden:
        return

    if user.is_anonymous and thread.is_unapproved:
        return

    if user.is_authenticated and thread.is_unapproved and thread.starter_id == user.id:
        raise AssertionError(
            "pinned queryset result for a user without moderator permissions "
            "is missing an unapproved thread started by them"
        )

    if (
        user.is_authenticated
        and category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "pinned queryset result for a user is missing a thread started by them"
        )


@pytest.mark.slow
def test_filter_threads_queryset(
    thread_factory,
    cache_versions,
    category,
    sibling_category,
    moderator,
    category_moderator,
    anonymous_user,
    user,
    other_user,
    category_guests_see_permission,
    category_guests_browse_permission,
    category_members_see_permission,
    category_members_browse_permission,
    category_moderators_see_permission,
    category_moderators_browse_permission,
):
    MATRIX = (
        (category, sibling_category),
        (moderator, category_moderator, anonymous_user, user, other_user),
        (False, True),
        (anonymous_user, user, other_user),
        (ThreadPinned.NONE, ThreadPinned.CATEGORY, ThreadPinned.EVERYWHERE),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_filter_threads_queryset_case(thread_factory, cache_versions, *args)


def check_filter_threads_queryset_case(
    thread_factory,
    cache_versions,
    category,
    user,
    started_only,
    starter,
    thread_pinned,
    thread_unapproved,
    thread_hidden,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(permissions, cache_versions)

    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = thread_factory(
        category,
        starter=starter if starter.is_authenticated else "Anon",
        pinned=thread_pinned,
        is_unapproved=thread_unapproved,
        is_hidden=thread_hidden,
    )

    queryset = filter_threads_queryset(
        permissions, categories.category_list, Thread.objects
    )
    if thread in queryset:
        assert_threads_queryset_contains(user, category, thread)
    else:
        assert_threads_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_threads_queryset_contains(user, category, thread):
    if category.slug == "sibling":
        raise AssertionError(
            "threads queryset result contains thread from category without permission"
        )

    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        return

    if thread.is_hidden:
        raise AssertionError(
            "threads queryset result for a user without moderator permissions "
            "contains a hidden thread"
        )

    if user.is_anonymous and thread.is_unapproved:
        raise AssertionError(
            "threads queryset result for an anonymous user contains "
            "an unapproved thread"
        )

    if user.is_authenticated and thread.is_unapproved and thread.starter_id != user.id:
        raise AssertionError(
            "threads queryset result for a user without moderator permissions "
            "contains an unapproved thread started by a different user"
        )


def assert_threads_queryset_not_contains(user, category, thread):
    if category.slug == "sibling":
        return

    if thread.is_hidden:
        return

    if user.is_anonymous and thread.is_unapproved:
        return

    if user.is_authenticated and thread.is_unapproved and thread.starter_id == user.id:
        raise AssertionError(
            "threads queryset result for a user without moderator "
            "permissions is missing an unapproved thread started by them"
        )

    if (
        user.is_authenticated
        and category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "threads queryset result for a user is missing a thread started by them"
        )
