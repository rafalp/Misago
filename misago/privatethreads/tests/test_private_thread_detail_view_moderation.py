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


def test_private_thread_detail_view_shows_thread_moderation_form_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        user=user,
        private_threads=True,
        is_global=False,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, THREAD_MODERATION_FORM_HTML)


def test_private_thread_detail_view_shows_thread_moderation_form_to_global_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, THREAD_MODERATION_FORM_HTML)


def test_private_thread_detail_view_shows_posts_moderation_form_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        user=user,
        private_threads=True,
        is_global=False,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_MODERATION_FORM_HTML)


def test_private_thread_detail_view_shows_posts_checkboxes_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        user=user,
        private_threads=True,
        is_global=False,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_CHECKBOX_HTML)


def test_private_thread_detail_view_shows_posts_checkboxes_to_global_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_CHECKBOX_HTML)


def test_private_thread_detail_view_shows_posts_moderation_form_to_global_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_MODERATION_FORM_HTML)


def test_private_thread_detail_view_shows_fixed_posts_moderation_form_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        user=user,
        private_threads=True,
        is_global=False,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_private_thread_detail_view_shows_fixed_posts_moderation_form_to_global_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_private_thread_detail_view_shows_post_moderation_form_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        user=user,
        private_threads=True,
        is_global=False,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POST_MODERATION_FORM_HTML)


def test_private_thread_detail_view_shows_post_moderation_form_to_global_moderator(
    moderator_client, user_private_thread
):
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, POST_MODERATION_FORM_HTML)


def test_private_thread_detail_view_doesnt_show_thread_moderation_form_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, THREAD_MODERATION_FORM_HTML)


def test_private_thread_detail_view_doesnt_show_posts_moderation_form_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, POSTS_MODERATION_FORM_HTML)


def test_private_thread_detail_view_doesnt_show_posts_checkboxes_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, POSTS_CHECKBOX_HTML)


def test_private_thread_detail_view_doesnt_show_fixed_posts_moderation_form_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, POSTS_MODERATION_FIXED_HTML)


def test_private_thread_detail_view_doesnt_show_post_moderation_form_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, POST_MODERATION_FORM_HTML)


def test_private_thread_detail_view_executes_thread_moderation_action(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_locked


def test_private_thread_detail_view_executes_thread_moderation_action_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Thread locked")

    user_private_thread.refresh_from_db()
    assert user_private_thread.is_locked


def test_private_thread_detail_view_executes_destructive_thread_moderation_action_with_confirmation(
    mocker, moderator_client, user_private_thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "delete"},
    )
    assert_contains(response, "Are you sure you want to delete this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse("misago:private-thread-list")

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()


def test_private_thread_detail_view_executes_destructive_thread_moderation_action_with_confirmation_in_htmx(
    mocker, moderator_client, user_private_thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.thread.synchronize_categories"
    )

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "delete"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete this thread?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "thread_moderation": "delete",
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response["hx-redirect"] == reverse("misago:private-thread-list")

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )

    with pytest.raises(Thread.DoesNotExist):
        user_private_thread.refresh_from_db()


def test_private_thread_detail_view_thread_moderation_shows_error_to_user(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
    )
    assert_contains(response, "Invalid moderation action.")


def test_private_thread_detail_view_thread_moderation_shows_error_to_user_in_htmx(
    user_client, user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "lock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_private_thread_detail_view_shows_error_for_invalid_thread_moderation_action(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "invalid"},
    )
    assert_contains(response, "Invalid moderation action.")


def test_private_thread_detail_view_shows_error_for_invalid_thread_moderation_action_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_private_thread_detail_view_shows_error_for_empty_thread_moderation_action(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": ""},
    )
    assert_contains(response, "Invalid moderation action.")


def test_private_thread_detail_view_shows_error_for_empty_thread_moderation_action_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"thread_moderation": ""},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_private_thread_detail_view_executes_posts_moderation_action(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    reply.refresh_from_db()
    assert reply.is_locked


def test_private_thread_detail_view_executes_posts_moderation_action_in_htmx(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts locked")

    reply.refresh_from_db()
    assert reply.is_locked


def test_private_thread_detail_view_executes_destructive_posts_moderation_action_with_confirmation(
    mocker, thread_reply_factory, moderator_client, user_private_thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "delete", "posts": [reply.id]},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"thread_id": user_private_thread.id, "slug": user_private_thread.slug},
    )

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_private_thread_detail_view_executes_destructive_posts_moderation_action_with_confirmation_in_htmx(
    mocker, thread_reply_factory, moderator_client, user_private_thread
):
    mock_synchronize_categories = mocker.patch(
        "misago.moderation.posts.synchronize_categories"
    )

    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "delete", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Are you sure you want to delete the selected posts?")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "delete",
            "posts": [reply.id],
            "confirm": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts deleted")

    mock_synchronize_categories.delay.assert_called_once_with(
        [user_private_thread.category_id]
    )

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()


def test_private_thread_detail_view_posts_moderation_action_shows_error_to_user(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = user_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")

    reply.refresh_from_db()
    assert not reply.is_locked


def test_private_thread_detail_view_posts_moderation_action_shows_error_to_user_in_htmx(
    thread_reply_factory, user_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = user_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "lock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)

    reply.refresh_from_db()
    assert not reply.is_locked


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_moderation_action(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "invalid", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_moderation_action_in_htmx(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "invalid", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_empty_moderation_action(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "", "posts": [reply.id]},
    )
    assert_contains(response, "Invalid moderation action.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_empty_moderation_action_in_htmx(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Invalid moderation action.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_validation_error_for_moderation_action(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [reply.id]},
    )
    assert_contains(response, "Posts are already unlocked.")


def test_private_thread_detail_view_posts_moderation_action_shows_validation_error_for_moderation_action_in_htmx(
    thread_reply_factory, moderator_client, user_private_thread
):
    reply = thread_reply_factory(user_private_thread, poster="DeletedUser")

    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [reply.id]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Posts are already unlocked.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_missing_posts_selection(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock"},
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_missing_posts_selection_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_empty_posts_selection(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": []},
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_empty_posts_selection_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": []},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_selection(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": "invalid"},
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_selection_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": "invalid"},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_ids_in_selection(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": ["invalid"]},
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_invalid_posts_ids_in_selection_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": ["invalid"]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_not_existing_posts_ids_in_selection(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [user_private_thread.last_post_id + 1]},
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_not_existing_posts_ids_in_selection_in_htmx(
    moderator_client, user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {"posts_moderation": "unlock", "posts": [user_private_thread.last_post_id + 1]},
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_other_thread_posts_ids_in_selection(
    moderator_client, user_private_thread, other_user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "unlock",
            "posts": [other_user_private_thread.last_post_id],
        },
    )
    assert_contains(response, "No valid posts selected.")


def test_private_thread_detail_view_posts_moderation_action_shows_error_for_other_thread_posts_ids_in_selection_in_htmx(
    moderator_client, user_private_thread, other_user_private_thread
):
    response = moderator_client.post(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        {
            "posts_moderation": "unlock",
            "posts": [other_user_private_thread.last_post_id],
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "No valid posts selected.", status_code=400)
