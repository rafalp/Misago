import pytest
from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned


@pytest.fixture
def mock_synchronize_categories(mocker):
    return mocker.patch("misago.moderation.threads.synchronize_categories")


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_everywhere_moderation_action_pins_unpinned_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_EVERYWHERE,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_everywhere_moderation_action_pins_pinned_category_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.EVERYWHERE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_EVERYWHERE,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_everywhere_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_everywhere", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already pinned.")

    assert not ThreadUpdate.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_category_moderation_action_pins_unpinned_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_CATEGORY,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_category_moderation_action_pins_pinned_everywhere_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.CATEGORY
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.PINNED_CATEGORY,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_pin_category_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "pin_category", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already pinned.")

    assert not ThreadUpdate.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unpin_moderation_action_unpins_pinned_everywhere_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.EVERYWHERE)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unpin_moderation_action_unpins_pinned_category_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, pinned=ThreadPinned.CATEGORY)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.pinned == ThreadPinned.NONE
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNPINNED,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unpin_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unpin", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unpinned.")

    assert not ThreadUpdate.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_lock_moderation_action_locks_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert response.status_code == 302

    thread.refresh_from_db()
    assert thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.LOCKED,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_lock_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, is_locked=True)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "lock", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already locked.")

    assert not ThreadUpdate.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unlock_moderation_action_unlocks_thread(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category, is_locked=True)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unlock", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert not thread.is_locked
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNLOCKED,
    )


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unlock_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unlock", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unlocked.")

    assert not ThreadUpdate.objects.exists()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_hide_moderation_action_hides_threads(
    thread_factory,
    moderator_client,
    moderator,
    default_category,
    mock_synchronize_categories,
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "hide", "threads": [thread.id]},
    )
    assert_contains(response, "Reason for hiding")
    assert_contains(response, "Hide threads")

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {
            "moderation": "hide",
            "threads": [thread.id],
            "moderation-hidden_reason": "Lorem ipsum",
            "confirm": True,
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert thread.is_hidden
    assert thread.hidden_at
    assert thread.hidden_by == moderator
    assert thread.hidden_by_name == moderator.username
    assert thread.hidden_by_slug == moderator.slug
    assert thread.hidden_reason == "Lorem ipsum"
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.HIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_hide_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_hidden=True)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "hide", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already hidden.")

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unhide_moderation_action_unhides_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_hidden=True)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unhide", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert not thread.is_hidden
    assert thread.hidden_at is None
    assert thread.hidden_by is None
    assert thread.hidden_by_name is None
    assert thread.hidden_by_slug is None
    assert thread.hidden_reason is None
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.UNHIDDEN,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_unhide_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "unhide", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already unhidden.")

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_approve_moderation_action_approves_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category, is_unapproved=True)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "approve", "threads": [thread.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:thread-list")

    thread.refresh_from_db()
    assert not thread.is_unapproved
    assert thread.has_updates

    ThreadUpdate.objects.get(
        thread=thread,
        action=ThreadUpdateActionName.APPROVED,
    )

    mock_synchronize_categories.delay.assert_called_once_with([default_category.id])


@override_dynamic_settings(index_view="categories")
def test_thread_list_view_approve_moderation_action_validates_threads(
    thread_factory, moderator_client, default_category, mock_synchronize_categories
):
    thread = thread_factory(default_category)

    response = moderator_client.post(
        reverse("misago:thread-list"),
        {"moderation": "approve", "threads": [thread.id]},
    )
    assert_contains(response, "Threads are already approved.")

    assert not ThreadUpdate.objects.exists()

    mock_synchronize_categories.delay.assert_not_called()
