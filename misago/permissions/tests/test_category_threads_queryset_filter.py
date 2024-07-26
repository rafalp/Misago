from itertools import product

from ...threads.models import Thread
from ...threads.enums import ThreadWeight
from ...threads.test import post_thread


def test_category_threads_queryset_includes_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset


def test_category_threads_queryset_includes_category_with_see_permission_and_delay_browse(
    category_threads_filter_factory,
    category,
    category_thread,
    category_members_see_permission,
    user,
):
    category.delay_browse_check = True
    category.save()

    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    assert category_thread in queryset


def test_category_threads_queryset_filter(
    category_threads_filter_factory,
    category,
    child_category,
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
    child_category_guests_see_permission,
    child_category_guests_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    child_category_moderators_see_permission,
    child_category_moderators_browse_permission,
    sibling_category_guests_see_permission,
    sibling_category_guests_browse_permission,
    sibling_category_members_see_permission,
    sibling_category_members_browse_permission,
    sibling_category_moderators_see_permission,
    sibling_category_moderators_browse_permission,
):
    MATRIX = (
        (moderator, category_moderator, anonymous_user, user, other_user),
        (category, child_category),
        (category, child_category, sibling_category),
        (False, True),
        (False, True),
        (anonymous_user, user, other_user),
        (0, 1, 2),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_category_thread_visibility(category_threads_filter_factory, *args)


def check_category_thread_visibility(
    category_threads_filter_factory,
    user,
    category,
    thread_category,
    list_children_threads,
    started_only,
    poster,
    thread_weight,
    thread_hidden,
    thread_unapproved,
):
    if category.list_children_threads != list_children_threads:
        category.list_children_threads = list_children_threads
        category.save()

    if thread_category.show_started_only != started_only:
        thread_category.show_started_only = started_only
        thread_category.save()

    thread = post_thread(
        thread_category,
        poster=poster if poster.is_authenticated else "Anon",
        is_global=thread_weight == 2,
        is_pinned=thread_weight == 1,
        is_hidden=thread_hidden,
        is_unapproved=thread_unapproved,
    )

    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter(Thread.objects)
    if thread in queryset:
        assert_queryset_contains(user, category, thread_category, thread)
    else:
        assert_queryset_not_contains(user, category, thread_category, thread)

    thread.delete()


def assert_queryset_contains(user, category, thread_category, thread):
    if thread_category.slug == "sibling":
        raise AssertionError(
            "queryset result contains a thread from the sibling category"
        )

    if category.slug == "child" and thread_category.slug == "parent":
        raise AssertionError(
            "queryset result contains a thread from the sibling category"
        )

    if (
        not category.list_children_threads
        and category.slug == "parent"
        and thread_category.slug == "child"
    ):
        raise AssertionError(
            "queryset result for the category with list_children_threads=False "
            "contains a thread from the child category "
        )

    if thread.weight == ThreadWeight.PINNED_GLOBALLY:
        raise AssertionError("queryset result contains a globally pinned thread")

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
        and thread_category.show_started_only
        and thread.weight != ThreadWeight.PINNED_IN_CATEGORY
    ):
        raise AssertionError(
            "queryset result for an anonymous user and category with "
            "show_started_only=true contains a thread that's not pinned in category"
        )

    if thread.weight == ThreadWeight.PINNED_IN_CATEGORY and category == thread_category:
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
        and thread_category.show_started_only
        and thread.weight != ThreadWeight.PINNED_IN_CATEGORY
        and thread.starter_id != user.id
    ):
        raise AssertionError(
            "queryset result for a category with show_started_only=true "
            "contains not pinned thread that's not started by the user"
        )


def assert_queryset_not_contains(user, category, thread_category, thread):
    if thread_category.slug == "sibling":
        return

    if category.slug == "child" and thread_category.slug == "parent":
        return

    if (
        not category.list_children_threads
        and category.slug == "parent"
        and thread_category.slug == "child"
    ):
        return

    if thread.weight == ThreadWeight.PINNED_GLOBALLY:
        return

    if thread.weight == ThreadWeight.PINNED_IN_CATEGORY and category == thread_category:
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
        and thread_category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "queryset result for a user is missing a thread started by them"
        )


def test_category_pinned_threads_queryset_includes_category_with_see_and_browse_permission(
    category_threads_filter_factory,
    category,
    category_pinned_thread,
    category_pinned_globally_thread,
    category_members_see_permission,
    category_members_browse_permission,
    user,
):
    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_thread in queryset
    assert category_pinned_globally_thread in queryset


def test_category_pinned_threads_queryset_includes_category_with_see_permission_and_delay_browse(
    category_threads_filter_factory,
    category,
    category_pinned_thread,
    category_pinned_globally_thread,
    category_members_see_permission,
    user,
):
    category.delay_browse_check = True
    category.save()

    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter_pinned(Thread.objects)
    assert category_pinned_thread in queryset
    assert category_pinned_globally_thread in queryset


def test_category_pinned_threads_queryset_filter(
    category_threads_filter_factory,
    category,
    child_category,
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
    child_category_guests_see_permission,
    child_category_guests_browse_permission,
    child_category_members_see_permission,
    child_category_members_browse_permission,
    child_category_moderators_see_permission,
    child_category_moderators_browse_permission,
    sibling_category_guests_see_permission,
    sibling_category_guests_browse_permission,
    sibling_category_members_see_permission,
    sibling_category_members_browse_permission,
    sibling_category_moderators_see_permission,
    sibling_category_moderators_browse_permission,
):
    MATRIX = (
        (moderator, category_moderator, anonymous_user, user, other_user),
        (category, child_category),
        (category, child_category, sibling_category),
        (False, True),
        (False, True),
        (anonymous_user, user, other_user),
        (0, 1, 2),
        (False, True),
        (False, True),
    )

    for args in product(*MATRIX):
        check_category_pinned_thread_visibility(category_threads_filter_factory, *args)


def check_category_pinned_thread_visibility(
    category_threads_filter_factory,
    user,
    category,
    thread_category,
    list_children_threads,
    started_only,
    poster,
    thread_weight,
    thread_hidden,
    thread_unapproved,
):
    if category.list_children_threads != list_children_threads:
        category.list_children_threads = list_children_threads
        category.save()

    if thread_category.show_started_only != started_only:
        thread_category.show_started_only = started_only
        thread_category.save()

    thread = post_thread(
        thread_category,
        poster=poster if poster.is_authenticated else "Anon",
        is_global=thread_weight == 2,
        is_pinned=thread_weight == 1,
        is_hidden=thread_hidden,
        is_unapproved=thread_unapproved,
    )

    threads_filter = category_threads_filter_factory(user, category)
    queryset = threads_filter.filter_pinned(Thread.objects)
    if thread in queryset:
        assert_pinned_queryset_contains(user, category, thread_category, thread)
    else:
        assert_pinned_queryset_not_contains(user, category, thread_category, thread)

    thread.delete()


def assert_pinned_queryset_contains(user, category, thread_category, thread):
    if thread.weight == ThreadWeight.NOT_PINNED:
        raise AssertionError(
            "pinned queryset result contains a thread that is not pinned"
        )

    if category != thread_category and thread.weight != ThreadWeight.PINNED_GLOBALLY:
        raise AssertionError(
            "pinned queryset result contains a thread from other category "
            "that is not globally pinned"
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
            "pinned queryset result for a user without moderator permissions contains "
            "an unapproved thread started by a different user"
        )


def assert_pinned_queryset_not_contains(user, category, thread_category, thread):
    if thread.weight == ThreadWeight.NOT_PINNED:
        return

    if category != thread_category and thread.weight != ThreadWeight.PINNED_GLOBALLY:
        return

    if user.is_authenticated and (
        user.slug == "moderator" or user.slug == "categorymoderator"
    ):
        raise AssertionError(
            "pinned queryset result for a moderator is missing a thread"
        )

    if thread.is_hidden:
        return

    if user.is_anonymous and thread.is_unapproved:
        return

    if user.is_authenticated and thread.is_unapproved and thread.starter_id == user.id:
        raise AssertionError(
            "pinned queryset result for a user without moderator permissions is "
            "missing an unapproved thread started by them"
        )

    if (
        user.is_authenticated
        and thread_category.show_started_only
        and thread.starter_id == user.id
    ):
        raise AssertionError(
            "pinned queryset result for a user is missing a thread started by them"
        )
