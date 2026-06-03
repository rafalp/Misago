from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..enums import ThreadPinned


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
