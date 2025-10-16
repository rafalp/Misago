from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains

MODERATION_FORM_HTML = '<form id="threads-moderation" method="post">'
MODERATION_FIXED_HTML = '<div class="fixed-moderation">'
DISABLED_CHECKBOX_HTML = '<input type="checkbox" disabled />'


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_noscript_moderation_form_to_category_moderator(
    user_client, user, default_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, MODERATION_FORM_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_noscript_moderation_form_to_global_moderator(
    moderator_client,
):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, MODERATION_FORM_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_fixed_moderation_form_to_category_moderator(
    user_client, user, default_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_fixed_moderation_form_to_global_moderator(
    moderator_client,
):
    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_show_moderation_to_user(user_client):
    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_doesnt_show_moderation_to_guest(user_client):
    response = user_client.get(reverse("misago:thread-list"))
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_threads_checkboxes_to_category_moderator(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(default_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_threads_checkboxes_to_global_moderator(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_disabled_threads_checkboxes_to_other_category_moderator(
    thread_factory, user_client, user, default_category, child_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.get(reverse("misago:thread-list"))
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_contains(response, DISABLED_CHECKBOX_HTML)


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_executes_single_stage_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_executes_single_stage_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-closed")

    thread.refresh_from_db()
    assert thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_executes_multi_stage_moderation_action(
    thread_factory, moderator_client, default_category, child_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": child_category.id,
            "confirm": "move",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.category == child_category


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_executes_multi_stage_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category, child_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "move", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Move threads")

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": child_category.id,
            "confirm": "move",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)

    thread.refresh_from_db()
    assert thread.category == child_category


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_moderation_shows_error_for_user(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_moderation_shows_error_for_user_in_htmx(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_moderation_shows_error_for_guest(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_moderation_shows_error_for_guest_in_htmx(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "invalid", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "invalid", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_empty_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_empty_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_empty_threads_selection(moderator_client):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": []},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_empty_threads_selection_in_htmx(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": []},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_threads_selection(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": "invalid"},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_threads_selection_in_htmx(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_threads_ids_in_selection(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": ["invalid"]},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_invalid_threads_ids_in_selection_in_htmx(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": ["invalid"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_not_existing_threads_ids_in_selection(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [42]},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_not_existing_threads_ids_in_selection_in_htmx(
    moderator_client,
):
    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [42]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_thread_in_selection_user_cant_moderate(
    thread_factory, default_category, child_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
    )
    assert_contains(
        response,
        f"Can&#x27;t moderate the &quot;{thread.title}&quot; thread",
    )

    thread.refresh_from_db()
    assert not thread.is_closed


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_shows_error_for_thread_in_selection_user_cant_moderate_in_htmx(
    thread_factory, default_category, child_category, user, user_client
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.post(
        reverse("misago:thread-list"),
        {"moderation": "close", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(
        response,
        f"Can&#x27;t moderate the &quot;{thread.title}&quot; thread",
    )

    thread.refresh_from_db()
    assert not thread.is_closed
