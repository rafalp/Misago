from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.enums import CategoryPermission
from ...permissions.models import CategoryGroupPermission, Moderator
from ...test import assert_contains, assert_not_contains
from ...threadevents.create import (
    create_added_member_thread_event,
    create_moved_thread_event,
    create_split_posts_from_thread_event,
    create_test_thread_event,
)


def test_thread_detail_view_doesnt_show_thread_event_to_anonymous_user_if_thread_flag_is_not_set(
    client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_thread_event_to_user_if_thread_flag_is_set(
    user_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_thread_event_to_category_moderator_if_thread_flag_is_not_set(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_thread_event_to_global_moderator_if_thread_flag_is_not_set(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_thread_event_to_anonymous_user_if_thread_flag_is_set(
    client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_thread_event_to_user_if_thread_flag_is_set(
    user_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_thread_event_to_category_moderator_if_thread_flag_is_set(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_thread_event_to_global_moderator_if_thread_flag_is_set(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_deleted_user_thread_event_to_anonymous_user(
    client, thread
):
    thread_event = create_test_thread_event(thread, "DeletedUser")

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_deleted_user_thread_event_to_user(
    user_client, thread
):
    thread_event = create_test_thread_event(thread, "DeletedUser")

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_deleted_user_thread_event_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, "DeletedUser")

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_deleted_user_thread_event_to_global_moderator(
    moderator_client, thread
):
    thread_event = create_test_thread_event(thread, "DeletedUser")

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_hidden_thread_event_to_anonymous_user(
    client, user, thread
):
    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_hidden_thread_event_to_user(
    user_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_hidden_thread_event_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_shows_hidden_thread_event_to_global_moderator(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")


def test_thread_detail_view_doesnt_show_hide_thread_event_button_to_anonymous_user(
    client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:thread-event-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_doesnt_show_hide_thread_event_button_to_user(
    user_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:thread-event-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_hide_thread_event_button_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_hide_thread_event_button_to_global_moderator(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-hide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_unhide_thread_event_button_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_unhide_thread_event_button_to_global_moderator(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)
    thread_event.is_hidden = True
    thread_event.save()

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-unhide",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_doesnt_show_delete_thread_event_button_to_anonymous_user(
    client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_doesnt_show_delete_thread_event_button_to_user(
    user_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_not_contains(
        response,
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_delete_thread_event_button_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


def test_thread_detail_view_shows_delete_thread_event_button_to_global_moderator(
    moderator_client, user, thread
):
    thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"UPDATE [{thread_event.id}]")
    assert_contains(
        response,
        reverse(
            "misago:thread-event-delete",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "thread_event_id": thread_event.id,
            },
        ),
    )


@override_dynamic_settings(
    thread_events_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_detail_view_shows_thread_events_on_first_page(
    thread_reply_factory, client, user, thread
):
    first_page_thread_event = create_test_thread_event(thread, user)

    for _ in range(6):
        thread_reply_factory(thread)

    last_page_thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"[{first_page_thread_event.id}]")
    assert_not_contains(response, f"[{last_page_thread_event.id}]")


@override_dynamic_settings(
    thread_events_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_detail_view_shows_thread_events_on_second_page(
    thread_reply_factory, client, user, thread
):
    for _ in range(4):
        thread_reply_factory(thread)

    first_page_thread_event = create_test_thread_event(thread, user)

    for _ in range(5):
        thread_reply_factory(thread)

    second_page_thread_event = create_test_thread_event(thread, user)

    for _ in range(2):
        thread_reply_factory(thread)

    last_page_thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2},
        )
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{first_page_thread_event.id}]")
    assert_contains(response, f"[{second_page_thread_event.id}]")
    assert_not_contains(response, f"[{last_page_thread_event.id}]")


@override_dynamic_settings(
    thread_events_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_detail_view_shows_thread_events_on_last_page(
    thread_reply_factory, client, user, thread
):
    for _ in range(4):
        thread_reply_factory(thread)

    first_page_thread_event = create_test_thread_event(thread, user)

    for _ in range(2):
        thread_reply_factory(thread)

    last_page_thread_event = create_test_thread_event(thread, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2},
        )
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{first_page_thread_event.id}]")
    assert_contains(response, f"[{last_page_thread_event.id}]")


@override_dynamic_settings(thread_updates_per_page=4)
def test_thread_detail_view_limits_displayed_thread_events_count(client, user, thread):
    thread_events = []
    for _ in range(5):
        thread_events.append(create_test_thread_event(thread, user))

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{thread_events[0].id}]")
    assert_contains(response, f"[{thread_events[1].id}]")
    assert_contains(response, f"[{thread_events[-1].id}]")


def test_thread_detail_view_displays_thread_event_with_other_category_context(
    client, guests_group, user, thread, other_category
):
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=guests_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=other_category,
        group=guests_group,
        permission=CategoryPermission.BROWSE,
    )

    create_moved_thread_event(thread, other_category, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_category.name)
    assert_contains(response, other_category.get_absolute_url())


def test_thread_detail_view_displays_thread_event_with_inaccessible_other_category_context(
    client, user, thread, other_category
):
    CategoryGroupPermission.objects.filter(category=other_category).delete()

    create_moved_thread_event(thread, other_category, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_category.name)
    assert_not_contains(response, other_category.get_absolute_url())


def test_thread_detail_view_displays_thread_event_with_other_thread_context(
    client, user, thread, other_thread
):
    create_split_posts_from_thread_event(thread, other_thread, actor=user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_thread.title)
    assert_contains(
        response,
        reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        ),
    )


def test_thread_detail_view_displays_thread_event_with_inaccessible_other_thread_context(
    client, user, thread, other_thread
):
    create_split_posts_from_thread_event(thread, other_thread, actor=user)

    thread.has_events = True
    thread.save()

    other_thread.is_hidden = True
    other_thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_thread.title)
    assert_not_contains(
        response,
        reverse(
            "misago:thread",
            kwargs={"thread_id": other_thread.id, "slug": other_thread.slug},
        ),
    )


def test_thread_detail_view_displays_thread_event_with_user_context(
    client, user, other_user, thread
):
    create_added_member_thread_event(thread, other_user, user)

    thread.has_events = True
    thread.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, other_user.username)
    assert_contains(response, other_user.get_absolute_url())
