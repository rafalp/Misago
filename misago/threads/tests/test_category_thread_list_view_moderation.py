import pytest

from ...conf.test import override_dynamic_settings
from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains
from ...threads.models import Thread

MODERATION_FORM_HTML = '<form id="threads-moderation" method="post">'
MODERATION_FIXED_HTML = '<div class="fixed-moderation">'
DISABLED_CHECKBOX_HTML = '<input type="checkbox" disabled />'


def test_category_thread_list_view_shows_noscript_moderation_form_to_category_moderator(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FORM_HTML)


def test_category_thread_list_view_shows_noscript_moderation_form_to_global_moderator(
    moderator_client, default_category
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FORM_HTML)


def test_category_thread_list_view_shows_fixed_moderation_form_to_category_moderator(
    user_client, user, default_category
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[default_category.id],
    )

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FIXED_HTML)


def test_category_thread_list_view_shows_fixed_moderation_form_to_global_moderator(
    moderator_client, default_category
):
    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, MODERATION_FIXED_HTML)


def test_category_thread_list_view_doesnt_show_moderation_to_user(
    user_client, default_category
):
    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_thread_list_view_doesnt_show_moderation_to_guest(
    user_client, default_category
):
    response = user_client.get(default_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_thread_list_view_doesnt_show_moderation_to_other_category_moderator(
    user_client, user, default_category, child_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(child_category.get_absolute_url())
    assert_not_contains(response, MODERATION_FORM_HTML)
    assert_not_contains(response, MODERATION_FIXED_HTML)


def test_category_thread_list_view_shows_threads_checkboxes_to_category_moderator(
    thread_factory, user_client, user, default_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(default_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_thread_list_view_shows_threads_checkboxes_to_global_moderator(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_not_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_thread_list_view_shows_disabled_threads_checkboxes_to_other_category_moderator(
    thread_factory, user_client, user, default_category, child_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.get(default_category.get_absolute_url())
    assert_contains(response, thread.title)
    assert_contains(response, "threads-list-item-col-checkbox")
    assert_contains(response, DISABLED_CHECKBOX_HTML)


def test_category_thread_list_view_executes_single_stage_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.is_locked


def test_category_thread_list_view_executes_single_stage_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, "thread-flags")
    assert_contains(response, "thread-flag-locked")

    thread.refresh_from_db()
    assert thread.is_locked


@pytest.mark.xfail(reason="delete thread moderation action not yet implemented")
def test_category_thread_list_view_executes_moderation_action_with_confirmation(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Delete threads")
    assert_contains(response, "Are you sure you want to delete selected threads?")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "Delete",
            "threads": [thread.id],
            "confirm": "delete",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


@pytest.mark.xfail(reason="delete thread moderation action not yet implemented")
def test_category_thread_list_view_executes_moderation_action_with_confirmation_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "delete", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Delete")
    assert_contains(response, "Are you sure you want to delete selected threads?")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "delete",
            "threads": [thread.id],
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


@pytest.mark.xfail(reason="move thread moderation action not yet implemented")
def test_category_thread_list_view_executes_moderation_action_with_form(
    thread_factory, moderator_client, default_category, child_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
    )
    assert_contains(response, "Move threads")
    assert_contains(response, "Move to")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": child_category.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == default_category.get_absolute_url()

    thread.refresh_from_db()
    assert thread.category == child_category


@pytest.mark.xfail(reason="move thread moderation action not yet implemented")
def test_category_thread_list_view_executes_moderation_action_with_form_in_htmx(
    thread_factory, moderator_client, default_category, child_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "move", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Move to")

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {
            "moderation": "move",
            "threads": [thread.id],
            "moderation-category": child_category.id,
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)

    thread.refresh_from_db()
    assert thread.category == child_category


def test_category_thread_list_view_moderation_shows_error_to_user(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_moderation_shows_error_to_user_in_htmx(
    thread_factory, user_client, default_category
):
    thread = thread_factory(default_category)

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_moderation_shows_error_to_guest(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_moderation_shows_error_to_guest_in_htmx(
    thread_factory, client, default_category
):
    thread = thread_factory(default_category)

    response = client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_shows_error_for_invalid_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "invalid", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_category_thread_list_view_shows_error_for_invalid_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "invalid", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_category_thread_list_view_shows_error_for_empty_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "", "threads": [thread.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_category_thread_list_view_shows_error_for_empty_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_category_thread_list_view_shows_error_for_empty_threads_selection(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": []},
    )
    assert_contains(response, "No valid threads selected.")


def test_category_thread_list_view_shows_error_for_empty_threads_selection_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": []},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.", status_code=400)


def test_category_thread_list_view_shows_error_for_invalid_threads_selection(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": "invalid"},
    )
    assert_contains(response, "No valid threads selected.")


def test_category_thread_list_view_shows_error_for_invalid_threads_selection_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.", status_code=400)


def test_category_thread_list_view_shows_error_for_invalid_threads_ids_in_selection(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": ["invalid"]},
    )
    assert_contains(response, "No valid threads selected.")


def test_category_thread_list_view_shows_error_for_invalid_threads_ids_in_selection_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": ["invalid"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.", status_code=400)


@override_dynamic_settings(threads_per_page=10)
def test_category_thread_list_view_shows_error_for_too_many_selected_threads(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": list(range(1, 20))},
    )
    assert_contains(response, "You can&#x27;t select more than 15 threads to moderate.")


@override_dynamic_settings(threads_per_page=10)
def test_category_thread_list_view_shows_error_for_too_many_selected_threads_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": list(range(1, 20))},
        headers={"hx-request": "true"},
    )
    assert_contains(
        response, "You can't select more than 15 threads to moderate.", status_code=400
    )


def test_category_thread_list_view_shows_error_for_not_existing_threads_ids_in_selection(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [42]},
    )
    assert_contains(response, "No valid threads selected.")


def test_category_thread_list_view_shows_error_for_not_existing_threads_ids_in_selection_in_htmx(
    moderator_client, default_category
):
    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [42]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid threads selected.", status_code=400)


def test_category_thread_list_view_shows_error_for_thread_in_selection_user_cant_moderate(
    thread_factory, user_client, user, default_category, child_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(
        response,
        f"Can&#x27;t moderate the &quot;{thread.title}&quot; thread",
    )

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_shows_error_for_thread_in_selection_user_cant_moderate_in_htmx(
    thread_factory, user_client, user, default_category, child_category
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )
    thread = thread_factory(child_category)

    response = user_client.post(
        default_category.get_absolute_url(),
        {"moderation": "lock", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(
        response,
        f'Can\'t moderate the \\"{thread.title}\\" thread.',
        status_code=400,
    )

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_shows_validation_error_from_moderation_action(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unlock", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unlocked.")

    thread.refresh_from_db()
    assert not thread.is_locked


def test_category_thread_list_view_shows_validation_error_from_moderation_action_in_htmx(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        default_category.get_absolute_url(),
        {"moderation": "unlock", "threads": [thread.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Threads are already unlocked.", status_code=400)

    thread.refresh_from_db()
    assert not thread.is_locked
