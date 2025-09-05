from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...html.element import html_element
from ...permissions.models import Moderator
from ...privatethreadmembers.models import PrivateThreadMember
from ...test import assert_contains, assert_not_contains
from ...threadupdates.create import create_test_thread_update


def test_private_thread_replies_view_shows_error_on_missing_permission(
    user, user_client, user_private_thread
):
    user.group.can_use_private_threads = False
    user.group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=403)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=403,
    )


def test_private_thread_replies_view_shows_error_to_anonymous_user(
    client, user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=403)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=403,
    )


def test_private_thread_replies_view_shows_error_to_user_who_is_not_member(
    user, user_client, user_private_thread
):
    PrivateThreadMember.objects.filter(user=user).delete()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, user_private_thread.title, status_code=404)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=404,
    )


def test_private_thread_replies_view_shows_thread_to_user(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_other_users_thread_to_user(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_thread_to_user_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_other_users_thread_to_user_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, other_user_private_thread.first_post.parsed)


def test_private_thread_replies_view_redirects_if_slug_is_invalid(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": "invalid"},
        ),
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )


def test_private_thread_replies_view_ignores_invalid_slug_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": "invalid"},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_redirects_to_last_page_if_page_number_is_too_large(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1000,
            },
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
    )


def test_private_thread_replies_view_shows_last_page_if_page_number_is_too_large_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1000,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, user_private_thread.first_post.parsed)


def test_private_thread_replies_view_shows_post_with_attachments(
    user_client,
    user_private_thread,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    text_attachment,
):
    post = user_private_thread.first_post

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_replies_view_shows_post_with_embed_attachments(
    user_client,
    user_private_thread,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    text_attachment,
):
    attachments = (
        image_attachment,
        image_thumbnail_attachment,
        video_attachment,
        text_attachment,
    )
    post = user_private_thread.first_post

    post.parsed = "<p>Hello world!</>"
    for attachment in attachments:
        post.parsed += html_element(
            "misago-attachment",
            attrs={
                "name": attachment.name,
                "slug": attachment.slug,
                "id": str(attachment.id),
            },
        )

    invalid_id = (
        max(
            image_attachment.id,
            image_thumbnail_attachment.id,
            video_attachment.id,
            text_attachment.id,
        )
        * 100
    )

    post.parsed += html_element(
        "misago-attachment",
        attrs={
            "name": "invalid-attachment.txt",
            "slug": "invalid-attachment-txt",
            "id": str(invalid_id),
        },
    )

    post.metadata = {
        "attachments": [
            image_attachment.id,
            image_thumbnail_attachment.id,
            video_attachment.id,
            text_attachment.id,
        ],
    }
    post.save()

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_replies_view_filters_thread_updates_using_user_permissions(
    user_client, user, user_private_thread
):
    visible_thread_update = create_test_thread_update(user_private_thread, user)
    hidden_thread_update = create_test_thread_update(
        user_private_thread, user, is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_not_contains(response, f"[{hidden_thread_update.id}]")


def test_private_thread_replies_view_shows_hidden_thread_updates_to_private_threads_moderator(
    user_client, user, user_private_thread
):
    Moderator.objects.create(
        private_threads=True,
        user=user,
        is_global=False,
    )

    visible_thread_update = create_test_thread_update(user_private_thread, user)
    hidden_thread_update = create_test_thread_update(
        user_private_thread, user, is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_contains(response, f"[{hidden_thread_update.id}]")


def test_private_thread_replies_view_shows_hidden_thread_updates_to_global_moderator(
    moderator_client, user, moderator, user_private_thread
):
    PrivateThreadMember.objects.create(thread=user_private_thread, user=moderator)

    visible_thread_update = create_test_thread_update(user_private_thread, user)
    hidden_thread_update = create_test_thread_update(
        user_private_thread, user, is_hidden=True
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_contains(response, f"[{hidden_thread_update.id}]")


@override_dynamic_settings(thread_updates_per_page=4)
def test_private_thread_replies_view_limits_thread_updates(
    user_client, user, user_private_thread
):
    thread_updates = []
    for _ in range(5):
        thread_updates.append(create_test_thread_update(user_private_thread, user))

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, f"[{thread_updates[0].id}]")
    assert_contains(response, f"[{thread_updates[1].id}]")
    assert_contains(response, f"[{thread_updates[-1].id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_replies_view_shows_thread_updates_on_first_page(
    thread_reply_factory, user_client, user, user_private_thread
):
    first_page_thread_update = create_test_thread_update(user_private_thread, user)

    for _ in range(6):
        thread_reply_factory(user_private_thread)

    last_page_thread_update = create_test_thread_update(user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": user_private_thread.id, "slug": user_private_thread.slug},
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_contains(response, f"[{first_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_replies_view_shows_thread_updates_on_second_page(
    thread_reply_factory, user_client, user, user_private_thread
):
    for _ in range(4):
        thread_reply_factory(user_private_thread)

    first_page_thread_update = create_test_thread_update(user_private_thread, user)

    for _ in range(5):
        thread_reply_factory(user_private_thread)

    second_page_thread_update = create_test_thread_update(user_private_thread, user)

    for _ in range(2):
        thread_reply_factory(user_private_thread)

    last_page_thread_update = create_test_thread_update(user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{second_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_private_thread_replies_view_shows_thread_updates_on_last_page(
    thread_reply_factory, user_client, user, user_private_thread
):
    for _ in range(4):
        thread_reply_factory(user_private_thread)

    first_page_thread_update = create_test_thread_update(user_private_thread, user)

    for _ in range(2):
        thread_reply_factory(user_private_thread)

    last_page_thread_update = create_test_thread_update(user_private_thread, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, user_private_thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{last_page_thread_update.id}]")


def test_private_thread_replies_view_shows_error_if_regular_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={"id": thread.id, "slug": thread.slug},
        ),
    )
    assert_not_contains(response, thread.title, status_code=404)
    assert_not_contains(response, thread.first_post.parsed, status_code=404)
