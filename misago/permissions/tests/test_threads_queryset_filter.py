from itertools import product


from ...categories.proxy import CategoriesProxy
from ...threads.enums import ThreadWeight
from ...threads.models import Thread
from ...threads.test import post_thread
from ..proxy import UserPermissionsProxy
from ..threads import filter_category_threads_queryset


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


def test_threads_queryset_filter(
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
        (0, 1, 2),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_thread_visibility(threads_filter_factory, *args)


def check_thread_visibility(
    threads_filter_factory,
    user,
    category,
    started_only,
    poster,
    thread_weight,
    thread_hidden,
    thread_unapproved,
):
    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = post_thread(
        category,
        poster=poster if poster.is_authenticated else "Anon",
        is_global=thread_weight == 2,
        is_pinned=thread_weight == 1,
        is_hidden=thread_hidden,
        is_unapproved=thread_unapproved,
    )

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter(Thread.objects)
    if thread in queryset:
        assert_queryset_contains(user, category, thread)
    else:
        assert_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_queryset_contains(user, category, thread):
    if thread.weight == ThreadWeight.PINNED_GLOBALLY:
        raise AssertionError(f"queryset result contains a globally pinned thread")

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
        and thread.weight != ThreadWeight.PINNED_IN_CATEGORY
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
        and not thread.weight
        and thread.starter_id != user.id
    ):
        raise AssertionError(
            "queryset result for a category with show_started_only=true "
            "contains not pinned thread that's not started by the user"
        )


def assert_queryset_not_contains(user, category, thread):
    if thread.weight == ThreadWeight.PINNED_GLOBALLY:
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
    category_pinned_globally_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_globally_thread in queryset


def test_threads_pinned_queryset_includes_category_with_see_permission_and_delay_browse(
    threads_filter_factory,
    category,
    category_pinned_globally_thread,
    category_members_see_permission,
    user,
):
    category.delay_browse_check = True
    category.save()

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_globally_thread in queryset


def test_threads_pinned_queryset_excludes_category_without_any_permissions(
    threads_filter_factory,
    category_pinned_globally_thread,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert not queryset.exists()


def test_threads_pinned_queryset_excludes_category_with_only_see_permission(
    threads_filter_factory,
    category_pinned_globally_thread,
    category_members_see_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert not queryset.exists()


def test_threads_pinned_queryset_combines_multiple_categories_with_see_and_browse_permission(
    threads_filter_factory,
    category_pinned_globally_thread,
    child_category_pinned_globally_thread,
    category_members_see_permission,
    category_members_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    user,
):
    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_globally_thread in queryset
    assert child_category_pinned_globally_thread in queryset


def test_threads_queryset_filter_pinned(
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
        (0, 1, 2),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_pinned_thread_visibility(threads_filter_factory, *args)


def check_pinned_thread_visibility(
    threads_filter_factory,
    user,
    category,
    started_only,
    poster,
    thread_weight,
    thread_hidden,
    thread_unapproved,
):
    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = post_thread(
        category,
        poster=poster if poster.is_authenticated else "Anon",
        is_global=thread_weight == 2,
        is_pinned=thread_weight == 1,
        is_hidden=thread_hidden,
        is_unapproved=thread_unapproved,
    )

    threads_filter = threads_filter_factory(user)
    queryset = threads_filter.filter_pinned(Thread.objects)
    if thread in queryset:
        assert_pinned_queryset_contains(user, category, thread)
    else:
        assert_pinned_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_pinned_queryset_contains(user, category, thread):
    if thread.weight != ThreadWeight.PINNED_GLOBALLY:
        raise AssertionError(
            "pinned queryset result contains a thread that's not pinned globally"
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
    if thread.weight != ThreadWeight.PINNED_GLOBALLY:
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


def test_filter_category_threads_queryset(
    cache_versions,
    category,
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
        (moderator, category_moderator, anonymous_user, user, other_user),
        (False, True),
        (anonymous_user, user, other_user),
        (0, 1, 2),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_category_thread_visibility(cache_versions, category, *args)


def check_category_thread_visibility(
    cache_versions,
    category,
    user,
    started_only,
    poster,
    thread_weight,
    thread_hidden,
    thread_unapproved,
):
    permissions = UserPermissionsProxy(user, cache_versions)
    categories = CategoriesProxy(permissions, cache_versions)

    if category.show_started_only != started_only:
        category.show_started_only = started_only
        category.save()

    thread = post_thread(
        category,
        poster=poster if poster.is_authenticated else "Anon",
        is_global=thread_weight == 2,
        is_pinned=thread_weight == 1,
        is_hidden=thread_hidden,
        is_unapproved=thread_unapproved,
    )

    queryset = filter_category_threads_queryset(
        permissions, categories.categories[category.id], category.thread_set
    )
    if thread in queryset:
        assert_category_threads_queryset_contains(user, category, thread)
    else:
        assert_category_threads_queryset_not_contains(user, category, thread)

    thread.delete()


def assert_category_threads_queryset_contains(user, category, thread):
    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        return

    if thread.is_hidden:
        raise AssertionError(
            "category threads queryset result for a user without moderator permissions "
            "contains a hidden thread"
        )

    if user.is_anonymous and thread.is_unapproved:
        raise AssertionError(
            "category threads queryset result for an anonymous user contains "
            "an unapproved thread"
        )

    if user.is_authenticated and thread.is_unapproved and thread.starter_id != user.id:
        raise AssertionError(
            "category threads queryset result for a user without moderator permissions "
            "contains an unapproved thread started by a different user"
        )


def assert_category_threads_queryset_not_contains(user, category, thread):
    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        raise AssertionError(
            "category threads queryset result for a moderator is missing a thread"
        )

    if thread.is_hidden:
        return

    if user.is_anonymous and thread.is_unapproved:
        return

    if user.is_authenticated and thread.is_unapproved and thread.starter_id == user.id:
        raise AssertionError(
            "category threads queryset result for a user without moderator "
            "permissions is missing an unapproved thread started by them"
        )

    if (
        user.is_authenticated
        and category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "category threads queryset result for a user is missing a thread started by them"
        )
