from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains
from ...threadupdates.create import (
    create_added_member_thread_update,
    create_moved_thread_update,
    create_split_thread_update,
    create_test_thread_update,
)


def test_private_thread_detail_view_shows_thread_update_to_user(
    user_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_thread_update_to_private_threads_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_thread_update_to_global_moderator(
    moderator_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_deleted_user_thread_update_to_user(
    user_client, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_deleted_user_thread_update_to_private_threads_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(other_user_private_thread, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_deleted_user_thread_update_to_global_moderator(
    moderator_client, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, "DeletedUser")

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_doesnt_show_hidden_thread_update_to_user(
    user_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(
        other_user_private_thread, user, is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_hidden_thread_update_to_category_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(
        other_user_private_thread, user, is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_shows_hidden_thread_update_to_global_moderator(
    moderator_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(
        other_user_private_thread, user, is_hidden=True
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")


def test_private_thread_detail_view_doesnt_show_hide_thread_update_button_to_user(
    user_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-update-hide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_hide_thread_update_button_to_private_threads_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-hide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_hide_thread_update_button_to_global_moderator(
    moderator_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-hide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_unhide_thread_update_button_to_category_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(
        other_user_private_thread, user, is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_unhide_thread_update_button_to_global_moderator(
    moderator_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(
        other_user_private_thread, user, is_hidden=True
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-unhide",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_delete_thread_update_button_to_user(
    user_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-update-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_delete_thread_update_button_to_category_moderator(
    user_client, user, other_user_private_thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        private_threads=True,
    )

    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_delete_thread_update_button_to_global_moderator(
    moderator_client, user, other_user_private_thread
):
    thread_update = create_test_thread_update(other_user_private_thread, user)

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{thread_update.id}]")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-update-delete",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "thread_update_id": thread_update.id,
            },
        ),
    )


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_detail_view_shows_thread_updates_on_first_page(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    first_page_thread_update = create_test_thread_update(
        other_user_private_thread, user
    )

    for _ in range(6):
        thread_reply_factory(other_user_private_thread)

    last_page_thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[{first_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_detail_view_shows_thread_updates_on_second_page(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    for _ in range(4):
        thread_reply_factory(other_user_private_thread)

    first_page_thread_update = create_test_thread_update(
        other_user_private_thread, user
    )

    for _ in range(5):
        thread_reply_factory(other_user_private_thread)

    second_page_thread_update = create_test_thread_update(
        other_user_private_thread, user
    )

    for _ in range(2):
        thread_reply_factory(other_user_private_thread)

    last_page_thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{second_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_detail_view_shows_thread_updates_on_last_page(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    for _ in range(4):
        thread_reply_factory(other_user_private_thread)

    first_page_thread_update = create_test_thread_update(
        other_user_private_thread, user
    )

    for _ in range(2):
        thread_reply_factory(other_user_private_thread)

    last_page_thread_update = create_test_thread_update(other_user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(thread_updates_per_page=4)
def test_private_thread_detail_view_limits_displayed_thread_updates_count(
    user_client, user, other_user_private_thread
):
    thread_updates = []
    for _ in range(5):
        thread_updates.append(
            create_test_thread_update(other_user_private_thread, user)
        )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[{thread_updates[0].id}]")
    assert_contains(response, f"[{thread_updates[1].id}]")
    assert_contains(response, f"[{thread_updates[-1].id}]")


def test_private_thread_detail_view_displays_thread_update_with_other_category_context(
    user_client, members_group, user, other_user_private_thread, other_category
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )

    create_moved_thread_update(other_user_private_thread, other_category, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_category.name)
    assert_contains(response, other_category.get_absolute_url())


def test_private_thread_detail_view_displays_thread_update_with_inaccessible_other_category_context(
    user_client, user, other_user_private_thread, other_category
):
    CategoryGroupPermission.objects.filter(category=other_category).delete()

    create_moved_thread_update(other_user_private_thread, other_category, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_category.name)
    assert_not_contains(response, other_category.get_absolute_url())


def test_private_thread_detail_view_displays_thread_update_with_other_thread_context(
    user_client, user, other_user_private_thread, other_thread
):
    create_split_thread_update(other_user_private_thread, other_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        ),
    )


def test_private_thread_detail_view_displays_thread_update_with_inaccessible_other_thread_context(
    user_client, user, other_user_private_thread, other_thread
):
    create_split_thread_update(other_user_private_thread, other_thread, user)

    other_thread.is_hidden = True
    other_thread.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        ),
    )


def test_private_thread_detail_view_displays_thread_update_with_user_context(
    user_client, user, other_user, other_user_private_thread
):
    create_added_member_thread_update(other_user_private_thread, other_user, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_user.username)
    assert_contains(response, other_user.get_absolute_url())
