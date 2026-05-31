import pytest
from django.urls import reverse

from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains
from ...threads.models import Post, Thread

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
    assert_contains(response, "Thread moved")

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


def test_thread_detail_view_shows_error_for_invalid_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "invalid"},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_detail_view_shows_error_for_invalid_thread_moderation_action_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_thread_detail_view_shows_error_for_empty_thread_moderation_action(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": ""},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_detail_view_shows_error_for_empty_thread_moderation_action_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"thread_moderation": ""},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_thread_detail_view_executes_posts_moderation_action(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_executes_posts_moderation_action_in_htmx(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts locked")

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_executes_posts_moderation_action_with_form(
    mocker, moderator_client, child_category, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
    )
    assert_contains(response, "Split posts into a new thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": child_category.id,
            "moderation-title": "New thread",
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

    reply.refresh_from_db()
    assert reply.category == child_category
    assert reply.thread != thread


def test_thread_detail_view_executes_posts_moderation_action_with_form_in_htmx(
    mocker, moderator_client, child_category, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "split", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "split",
            "posts": [reply.id],
            "moderation-category": child_category.id,
            "moderation-title": "New thread",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts were split into a new thread.")

    mock_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id, child_category.id]
    )

    reply.refresh_from_db()
    assert reply.category == child_category
    assert reply.thread == Thread.objects.get(
        slug="new-thread", category=child_category
    )


def test_thread_detail_view_executes_destructive_posts_moderation_action_with_confirmation(
    mocker, moderator_client, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "delete", "posts": [reply.id]},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_thread_detail_view_executes_destructive_posts_moderation_action_with_confirmation_in_htmx(
    mocker, moderator_client, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "delete", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts deleted")

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_thread_detail_view_posts_moderation_action_shows_error_to_user(
    user_client, thread, reply
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_posts_moderation_action_shows_error_to_user_in_htmx(
    user_client, thread, reply
):
    response = user_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_posts_moderation_action_shows_error_to_guest(
    client, thread, reply
):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_posts_moderation_action_shows_error_to_guest_in_htmx(
    client, thread, reply
):
    response = client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "lock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    reply.refresh_from_db()
    assert not reply.is_locked


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_moderation_action(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "invalid", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_moderation_action_in_htmx(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "invalid", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_empty_moderation_action(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_empty_moderation_action_in_htmx(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_validation_error_for_moderation_action(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unlocked.")


def test_thread_detail_view_posts_moderation_action_shows_validation_error_for_moderation_action_in_htmx(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts are already unlocked.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_missing_posts_selection(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock"},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_missing_posts_selection_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_empty_posts_selection(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": []},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_empty_posts_selection_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": []},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_selection(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": "invalid"},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_selection_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_ids_in_selection(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": ["invalid"]},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_ids_in_selection_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": ["invalid"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_not_existing_posts_ids_in_selection(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [thread.last_post_id + 1]},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_not_existing_posts_ids_in_selection_in_htmx(
    moderator_client, thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [thread.last_post_id + 1]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_posts_moderation_action_shows_error_for_other_thread_posts_ids_in_selection(
    moderator_client, thread, user_thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [user_thread.last_post_id]},
    )
    assert_contains(response, "No valid posts selected.")


def test_thread_detail_view_posts_moderation_action_shows_error_for_other_thread_posts_ids_in_selection_in_htmx(
    moderator_client, thread, user_thread
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"posts_moderation": "unlock", "posts": [user_thread.last_post_id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_thread_detail_view_executes_post_moderation_action(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "lock", "post": reply.id},
    )
    assert response.status_code == 302
    assert (
        response["location"]
        == reverse(
            "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
        )
        + f"#post-{reply.id}"
    )

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_executes_post_moderation_action_in_htmx(
    moderator_client, thread, reply
):
    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "lock", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post locked")

    reply.refresh_from_db()
    assert reply.is_locked


def test_thread_detail_view_executes_post_moderation_action_with_form(
    mocker, moderator_client, child_category, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.post.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": [reply.id]},
    )
    assert_contains(response, "Split post into a new thread")
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": [reply.id],
            "moderation-category": child_category.id,
            "moderation-title": "New thread",
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

    reply.refresh_from_db()
    assert reply.category == child_category
    assert reply.thread != thread


def test_thread_detail_view_executes_post_moderation_action_with_form_in_htmx(
    mocker, moderator_client, child_category, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.post.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "split", "post": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Category")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "split",
            "post": [reply.id],
            "moderation-category": child_category.id,
            "moderation-title": "New thread",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post was split into a new thread.")

    mock_synchronize_categories.delay.assert_called_once_with(
        [thread.category_id, child_category.id]
    )

    reply.refresh_from_db()
    assert reply.category == child_category
    assert reply.thread == Thread.objects.get(
        slug="new-thread", category=child_category
    )


def test_thread_detail_view_executes_destructive_post_moderation_action_with_confirmation(
    mocker, moderator_client, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.post.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "delete", "post": reply.id},
    )
    assert_contains(response, "Are you sure you want to delete the selected post?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "delete",
            "post": reply.id,
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_thread_detail_view_executes_destructive_post_moderation_action_with_confirmation_in_htmx(
    mocker, moderator_client, thread, reply
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.post.synchronize_categories"
    )

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {"post_moderation": "delete", "post": reply.id},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete the selected post?")

    response = moderator_client.post(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        {
            "post_moderation": "delete",
            "post": reply.id,
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post deleted")

    mock_synchronize_categories.delay.assert_called_once_with([thread.category_id])

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()
