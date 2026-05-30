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
