from django.urls import reverse

from ...permissions.models import Moderator, CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_thread_replies_view_shows_error_on_missing_permission(
    guests_group, client, thread, post
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, thread.title, status_code=404)


def test_thread_replies_view_filters_posts_using_user_permissions(
    client, thread, post, unapproved_reply
):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_not_contains(response, unapproved_reply.parsed)


def test_thread_replies_view_redirects_if_slug_is_invalid(moderator_client, thread):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": "invalid"}),
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


def test_thread_replies_view_ignores_invalid_slug_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": "invalid"}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, post.parsed)


def test_thread_replies_view_redirects_to_last_page_if_page_number_is_too_large(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread", kwargs={"id": thread.id, "slug": thread.slug, "page": 1000}
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"id": thread.id, "slug": thread.slug}
    )


def test_thread_replies_view_shows_last_page_if_page_number_is_too_large_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse(
            "misago:thread", kwargs={"id": thread.id, "slug": thread.slug, "page": 1000}
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_anonymous_user(client, thread, post):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_user(user_client, thread, post):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_category_moderator(
    default_category, user, user_client, thread, post
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_global_moderator(moderator_client, thread, post):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_anonymous_user_in_htmx(client, thread, post):
    response = client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_user_in_htmx(user_client, thread, post):
    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_category_moderator_in_htmx(
    default_category, user, user_client, thread, post
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_global_moderator_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_anonymous_unapproved_reply_to_category_moderator(
    default_category, user, user_client, thread, post, unapproved_reply
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, unapproved_reply.parsed)


def test_thread_replies_view_shows_anonymous_unapproved_reply_to_global_moderator(
    moderator_client, thread, post, unapproved_reply
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, unapproved_reply.parsed)


def test_thread_replies_view_shows_other_users_unapproved_reply_to_category_moderator(
    default_category, user, user_client, thread, post, other_user_unapproved_reply
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    response = user_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, other_user_unapproved_reply.parsed)


def test_thread_replies_view_shows_other_users_unapproved_reply_to_global_moderator(
    moderator_client, thread, post, other_user_unapproved_reply
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, other_user_unapproved_reply.parsed)


def test_thread_replies_view_shows_error_if_private_thread_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        ),
    )
    assert_not_contains(response, user_private_thread.title, status_code=404)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=404,
    )
