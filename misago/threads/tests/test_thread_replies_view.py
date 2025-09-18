from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...html.element import html_element
from ...permissions.models import Moderator, CategoryGroupPermission
from ...test import assert_contains, assert_not_contains
from ...threadupdates.create import create_test_thread_update


def test_thread_replies_view_shows_error_on_missing_permission(
    guests_group, client, thread
):
    CategoryGroupPermission.objects.filter(group=guests_group).delete()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, thread.title, status_code=404)


def test_thread_replies_view_filters_posts_using_user_permissions(
    client, thread, post, unapproved_reply
):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_not_contains(response, unapproved_reply.parsed)


def test_thread_replies_view_redirects_if_slug_is_invalid(moderator_client, thread):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": "invalid"}),
    )
    assert response.status_code == 301
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_replies_view_ignores_invalid_slug_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": "invalid"}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, post.parsed)


def test_thread_replies_view_redirects_to_last_page_if_page_number_is_too_large(
    moderator_client, thread
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 1000},
        ),
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}
    )


def test_thread_replies_view_shows_last_page_if_page_number_is_too_large_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 1000},
        ),
        headers={"hx-request": "true"},
    )
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_anonymous_user(client, thread, post):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_user(user_client, thread, post):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_global_moderator(moderator_client, thread, post):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_anonymous_user_in_htmx(client, thread, post):
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_user_in_htmx(user_client, thread, post):
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)


def test_thread_replies_view_shows_to_global_moderator_in_htmx(
    moderator_client, thread, post
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, unapproved_reply.parsed)


def test_thread_replies_view_shows_anonymous_unapproved_reply_to_global_moderator(
    moderator_client, thread, post, unapproved_reply
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
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
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, other_user_unapproved_reply.parsed)


def test_thread_replies_view_shows_other_users_unapproved_reply_to_global_moderator(
    moderator_client, thread, post, other_user_unapproved_reply
):
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug}),
        headers={"hx-request": "true"},
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, other_user_unapproved_reply.parsed)


def test_thread_replies_view_shows_post_with_attachments(
    client,
    thread,
    post,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    text_attachment,
):
    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_thread_replies_view_shows_post_with_embed_attachments(
    client,
    thread,
    post,
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

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())
    assert_contains(response, video_attachment.get_absolute_url())
    assert_contains(response, text_attachment.get_absolute_url())


def test_thread_replies_view_filters_thread_updates_using_user_permissions(
    client, user, thread
):
    visible_thread_update = create_test_thread_update(thread, user)
    hidden_thread_update = create_test_thread_update(thread, user, is_hidden=True)

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_not_contains(response, f"[{hidden_thread_update.id}]")


def test_thread_replies_view_shows_hidden_thread_updates_to_category_moderator(
    user_client, user, default_category, thread
):
    Moderator.objects.create(
        categories=[default_category.id],
        user=user,
        is_global=False,
    )

    visible_thread_update = create_test_thread_update(thread, user)
    hidden_thread_update = create_test_thread_update(thread, user, is_hidden=True)

    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_contains(response, f"[{hidden_thread_update.id}]")


def test_thread_replies_view_shows_hidden_thread_updates_to_global_moderator(
    moderator_client, user, thread
):
    visible_thread_update = create_test_thread_update(thread, user)
    hidden_thread_update = create_test_thread_update(thread, user, is_hidden=True)

    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"[{visible_thread_update.id}]")
    assert_contains(response, f"[{hidden_thread_update.id}]")


@override_dynamic_settings(thread_updates_per_page=4)
def test_thread_replies_view_limits_thread_updates(client, user, thread):
    thread_updates = []
    for _ in range(5):
        thread_updates.append(create_test_thread_update(thread, user))

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{thread_updates[0].id}]")
    assert_contains(response, f"[{thread_updates[1].id}]")
    assert_contains(response, f"[{thread_updates[-1].id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_replies_view_shows_thread_updates_on_first_page(
    thread_reply_factory, client, user, thread
):
    first_page_thread_update = create_test_thread_update(thread, user)

    for _ in range(6):
        thread_reply_factory(thread)

    last_page_thread_update = create_test_thread_update(thread, user)

    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, thread.title)
    assert_contains(response, f"[{first_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_replies_view_shows_thread_updates_on_second_page(
    thread_reply_factory, client, user, thread
):
    for _ in range(4):
        thread_reply_factory(thread)

    first_page_thread_update = create_test_thread_update(thread, user)

    for _ in range(5):
        thread_reply_factory(thread)

    second_page_thread_update = create_test_thread_update(thread, user)

    for _ in range(2):
        thread_reply_factory(thread)

    last_page_thread_update = create_test_thread_update(thread, user)

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2},
        )
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{second_page_thread_update.id}]")
    assert_not_contains(response, f"[{last_page_thread_update.id}]")


@override_dynamic_settings(
    thread_updates_per_page=4, posts_per_page=5, posts_per_page_orphans=1
)
def test_thread_replies_view_shows_thread_updates_on_last_page(
    thread_reply_factory, client, user, thread
):
    for _ in range(4):
        thread_reply_factory(thread)

    first_page_thread_update = create_test_thread_update(thread, user)

    for _ in range(2):
        thread_reply_factory(thread)

    last_page_thread_update = create_test_thread_update(thread, user)

    response = client.get(
        reverse(
            "misago:thread",
            kwargs={"thread_id": thread.id, "slug": thread.slug, "page": 2},
        )
    )
    assert_contains(response, thread.title)
    assert_not_contains(response, f"[{first_page_thread_update.id}]")
    assert_contains(response, f"[{last_page_thread_update.id}]")


def test_thread_replies_view_shows_error_if_private_thread_is_accessed(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        ),
    )
    assert_not_contains(response, user_private_thread.title, status_code=404)
    assert_not_contains(
        response,
        user_private_thread.first_post.parsed,
        status_code=404,
    )
