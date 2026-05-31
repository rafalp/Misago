import pytest
from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains
from ...threads.models import Thread

THREAD_MODERATION_FORM_HTML = 'name="thread_moderation"'
POSTS_MODERATION_FORM_HTML = 'name="posts_moderation'
POSTS_MODERATION_FIXED_HTML = '<div class="fixed-moderation">'
POSTS_CHECKBOX_HTML = "posts-feed-item-checkbox"
POST_MODERATION_FORM_HTML = 'name="post_moderation"'


def test_thread_detail_view_shows_thread_moderation_form_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        categories=[thread.category_id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, THREAD_MODERATION_FORM_HTML)


def test_thread_detail_view_shows_thread_moderation_form_to_global_moderator(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, THREAD_MODERATION_FORM_HTML)


def test_thread_detail_view_shows_posts_moderation_form_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        categories=[thread.category_id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_MODERATION_FORM_HTML)


def test_thread_detail_view_shows_posts_checkboxes_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        categories=[thread.category_id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_CHECKBOX_HTML)


def test_thread_detail_view_shows_posts_checkboxes_to_global_moderator(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_CHECKBOX_HTML)


def test_thread_detail_view_shows_posts_moderation_form_to_global_moderator(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_MODERATION_FORM_HTML)


def test_thread_detail_view_shows_fixed_posts_moderation_form_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        categories=[thread.category_id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_thread_detail_view_shows_fixed_posts_moderation_form_to_global_moderator(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_thread_detail_view_shows_post_moderation_form_to_category_moderator(
    user_client, user, thread
):
    Moderator.objects.create(
        categories=[thread.category_id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POST_MODERATION_FORM_HTML)


def test_thread_detail_view_shows_post_moderation_form_to_global_moderator(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, POST_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_thread_moderation_form_to_user(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, THREAD_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_posts_moderation_form_to_user(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_posts_checkboxes_to_user(user_client, thread):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_CHECKBOX_HTML)


def test_thread_detail_view_doesnt_show_fixed_posts_moderation_form_to_user(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_thread_detail_view_doesnt_show_post_moderation_form_to_user(
    user_client, thread
):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POST_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_thread_moderation_form_to_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, THREAD_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_posts_moderation_form_to_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_MODERATION_FORM_HTML)


def test_thread_detail_view_doesnt_show_posts_checkboxes_to_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_CHECKBOX_HTML)


def test_thread_detail_view_doesnt_show_fixed_posts_moderation_form_to_guest(
    client, thread
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_thread_detail_view_doesnt_show_post_moderation_form_to_guest(client, thread):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, POST_MODERATION_FORM_HTML)


def test_thread_detail_view_executes_thread_moderation_action(moderator_client, thread):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    thread.refresh_from_db()
    assert thread.is_locked


def test_thread_detail_view_executes_thread_moderation_action_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Thread locked")

    thread.refresh_from_db()
    assert thread.is_locked


def test_thread_detail_view_executes_thread_moderation_action_with_form(
    mocker, moderator_client, child_category, thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
    )
    assert_contains(response, "Move thread")
    assert_contains(response, "Move to")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": child_category.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id, child_category.id]
    )

    thread.refresh_from_db()
    assert thread.category == child_category


def test_thread_detail_view_executes_thread_moderation_action_with_form_in_htmx(
    mocker, moderator_client, child_category, thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "move"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Move to")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "move",
            "moderation-category": child_category.id,
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, child_category.name)

    mock_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id, child_category.id]
    )

    thread.refresh_from_db()
    assert thread.category == child_category


def test_thread_detail_view_executes_destructive_thread_moderation_action_with_confirmation(
    mocker, moderator_client, default_category, thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "delete"},
    )
    assert_contains(response, "Are you sure you want to delete this thread?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:category-thread-list",
        kwargs={"category_id": default_category.id, "slug": default_category.slug},
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


def test_thread_detail_view_executes_destructive_thread_moderation_action_with_confirmation_in_htmx(
    mocker, moderator_client, default_category, thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "delete"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete this thread?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response["hx-redirect"] == reverse(
        "misago:category-thread-list",
        kwargs={"category_id": default_category.id, "slug": default_category.slug},
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Thread.DoesNotExist):
        thread.refresh_from_db()


def test_thread_detail_view_thread_moderation_shows_error_to_user(user_client, thread):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_locked


def test_thread_detail_view_thread_moderation_shows_error_to_user_in_htmx(
    user_client, thread
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    thread.refresh_from_db()
    assert not thread.is_locked


def test_thread_detail_view_thread_moderation_shows_error_to_guest(client, thread):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
    )
    assert_contains(response, "Invalid moderation action.")

    thread.refresh_from_db()
    assert not thread.is_locked


def test_thread_detail_view_thread_moderation_shows_error_to_guest_in_htmx(
    client, thread
):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "lock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    thread.refresh_from_db()
    assert not thread.is_locked


def test_thread_list_view_shows_error_for_invalid_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "invalid"},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_list_view_shows_error_for_invalid_thread_moderation_action_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_thread_list_view_shows_error_for_empty_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": ""},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_list_view_shows_error_for_empty_thread_moderation_action_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": ""},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)
