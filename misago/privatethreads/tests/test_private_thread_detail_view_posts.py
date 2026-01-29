from django.utils.crypto import get_random_string
from django.urls import reverse
from django.utils import timezone

from ...conf.test import override_dynamic_settings
from ...likes.like import like_post
from ...permissions.enums import CanSeePostEdits, CanSeePostLikes, CategoryPermission
from ...permissions.models import CategoryGroupPermission
from ...test import assert_contains, assert_not_contains


def test_private_thread_detail_view_returns_redirect_to_first_page_if_page_is_out_of_range(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_returns_redirect_to_last_page_if_page_is_out_of_range(
    thread_reply_factory, user_client, user_private_thread
):
    for i in range(1, 20):
        thread_reply_factory(user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "page": 4,
        },
    )


def test_private_thread_detail_view_returns_redirect_if_explicit_first_page_is_given(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )


def test_private_thread_detail_view_ignores_explicit_first_page_in_htmx(
    user_client, user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 1,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_first_page_in_multi_page_thread(
    thread_reply_factory, user_client, user_private_thread
):
    for i in range(1, 7):
        thread_reply_factory(user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )

    assert_contains(response, "Reply no. 1")
    assert_contains(response, "Reply no. 2")
    assert_contains(response, "Reply no. 3")
    assert_contains(response, "Reply no. 4")
    assert_not_contains(response, "Reply no. 5")
    assert_not_contains(response, "Reply no. 6")


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_middle_page_in_multi_page_thread(
    thread_reply_factory, user_client, user_private_thread
):
    for i in range(1, 12):
        thread_reply_factory(user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )

    assert_not_contains(response, "Reply no. 1")
    assert_not_contains(response, "Reply no. 2")
    assert_not_contains(response, "Reply no. 3")
    assert_not_contains(response, "Reply no. 4")
    assert_contains(response, "Reply no. 5")
    assert_contains(response, "Reply no. 6")
    assert_contains(response, "Reply no. 7")
    assert_contains(response, "Reply no. 8")
    assert_contains(response, "Reply no. 9")
    assert_not_contains(response, "Reply no. 10")
    assert_not_contains(response, "Reply no. 11")


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_last_page_in_multi_page_thread(
    thread_reply_factory, user_client, user_private_thread
):
    for i in range(1, 7):
        thread_reply_factory(user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )

    assert_not_contains(response, "Reply no. 1")
    assert_not_contains(response, "Reply no. 2")
    assert_not_contains(response, "Reply no. 3")
    assert_not_contains(response, "Reply no. 4")
    assert_contains(response, "Reply no. 5")
    assert_contains(response, "Reply no. 6")


def test_private_thread_detail_view_shows_deleted_user_post_to_user(
    thread_reply_factory, user_client, user_private_thread
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_deleted_user_post_to_moderator(
    thread_reply_factory, moderator_client, user_private_thread
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_user_post_to_user(
    thread_reply_factory, user_client, user_private_thread, user
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
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
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_other_user_post_to_user(
    thread_reply_factory, user_client, user_private_thread, other_user
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=other_user
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
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_user_post_to_moderator(
    thread_reply_factory, moderator_client, user_private_thread, user
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_deleted_user_hidden_post_to_user(
    thread_reply_factory, user_client, user_private_thread
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
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
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_private_thread_detail_view_shows_deleted_user_hidden_post_to_moderator(
    thread_reply_factory, moderator_client, user_private_thread
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
    )
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_user_hidden_post_to_user(
    thread_reply_factory, user_client, user_private_thread, user
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user, is_hidden=True
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
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_private_thread_detail_view_shows_other_user_hidden_post_to_user(
    thread_reply_factory, user_client, user_private_thread, other_user
):
    post = thread_reply_factory(
        user_private_thread,
        original=get_random_string(12),
        poster=other_user,
        is_hidden=True,
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
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_private_thread_detail_view_shows_user_hidden_post_to_moderator(
    thread_reply_factory, moderator_client, user_private_thread, user
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user, is_hidden=True
    )
    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_private_thread_detail_view_shows_post_with_all_attachment_types(
    thread_reply_factory,
    user_client,
    user_private_thread,
    text_attachment,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    broken_text_attachment,
    broken_image_attachment,
    broken_image_thumbnail_attachment,
    broken_video_attachment,
    user_text_attachment,
    user_image_attachment,
    user_image_thumbnail_attachment,
    user_video_attachment,
    user_broken_text_attachment,
    user_broken_image_attachment,
    user_broken_image_thumbnail_attachment,
    user_broken_video_attachment,
    other_user_text_attachment,
    other_user_image_attachment,
    other_user_image_thumbnail_attachment,
    other_user_video_attachment,
    other_user_broken_text_attachment,
    other_user_broken_image_attachment,
    other_user_broken_image_thumbnail_attachment,
    other_user_broken_video_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    text_attachment.associate_with_post(post)
    text_attachment.save()

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    broken_text_attachment.associate_with_post(post)
    broken_text_attachment.save()

    broken_image_attachment.associate_with_post(post)
    broken_image_attachment.save()

    broken_image_thumbnail_attachment.associate_with_post(post)
    broken_image_thumbnail_attachment.save()

    broken_video_attachment.associate_with_post(post)
    broken_video_attachment.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    user_image_thumbnail_attachment.associate_with_post(post)
    user_image_thumbnail_attachment.save()

    user_video_attachment.associate_with_post(post)
    user_video_attachment.save()

    user_broken_text_attachment.associate_with_post(post)
    user_broken_text_attachment.save()

    user_broken_image_attachment.associate_with_post(post)
    user_broken_image_attachment.save()

    user_broken_image_thumbnail_attachment.associate_with_post(post)
    user_broken_image_thumbnail_attachment.save()

    user_broken_video_attachment.associate_with_post(post)
    user_broken_video_attachment.save()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    other_user_image_attachment.associate_with_post(post)
    other_user_image_attachment.save()

    other_user_image_thumbnail_attachment.associate_with_post(post)
    other_user_image_thumbnail_attachment.save()

    other_user_video_attachment.associate_with_post(post)
    other_user_video_attachment.save()

    other_user_broken_text_attachment.associate_with_post(post)
    other_user_broken_text_attachment.save()

    other_user_broken_image_attachment.associate_with_post(post)
    other_user_broken_image_attachment.save()

    other_user_broken_image_thumbnail_attachment.associate_with_post(post)
    other_user_broken_image_thumbnail_attachment.save()

    other_user_broken_video_attachment.associate_with_post(post)
    other_user_broken_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())

    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())

    assert_contains(response, image_thumbnail_attachment.name)
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, video_attachment.name)
    assert_contains(response, video_attachment.get_absolute_url())

    assert_contains(response, broken_text_attachment.name)
    assert_contains(response, broken_text_attachment.get_absolute_url())

    assert_contains(response, broken_image_attachment.name)
    assert_contains(response, broken_image_attachment.get_absolute_url())

    assert_contains(response, broken_image_thumbnail_attachment.name)
    assert_contains(response, broken_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, broken_video_attachment.name)
    assert_contains(response, broken_video_attachment.get_absolute_url())

    assert_contains(response, user_text_attachment.name)
    assert_contains(response, user_text_attachment.get_absolute_url())

    assert_contains(response, user_image_attachment.name)
    assert_contains(response, user_image_attachment.get_absolute_url())

    assert_contains(response, user_image_thumbnail_attachment.name)
    assert_contains(response, user_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, user_video_attachment.name)
    assert_contains(response, user_video_attachment.get_absolute_url())

    assert_contains(response, user_broken_text_attachment.name)
    assert_contains(response, user_broken_text_attachment.get_absolute_url())

    assert_contains(response, user_broken_image_attachment.name)
    assert_contains(response, user_broken_image_attachment.get_absolute_url())

    assert_contains(response, user_broken_image_thumbnail_attachment.name)
    assert_contains(response, user_broken_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, user_broken_video_attachment.name)
    assert_contains(response, user_broken_video_attachment.get_absolute_url())

    assert_contains(response, other_user_text_attachment.name)
    assert_contains(response, other_user_text_attachment.get_absolute_url())

    assert_contains(response, other_user_image_attachment.name)
    assert_contains(response, other_user_image_attachment.get_absolute_url())

    assert_contains(response, other_user_image_thumbnail_attachment.name)
    assert_contains(response, other_user_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, other_user_video_attachment.name)
    assert_contains(response, other_user_video_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_text_attachment.name)
    assert_contains(response, other_user_broken_text_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_image_attachment.name)
    assert_contains(response, other_user_broken_image_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_image_thumbnail_attachment.name)
    assert_contains(
        response, other_user_broken_image_thumbnail_attachment.get_absolute_url()
    )

    assert_contains(response, other_user_broken_video_attachment.name)
    assert_contains(response, other_user_broken_video_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_deleted_user_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    text_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_deleted_user_post_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    text_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_other_user_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=other_user
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_post_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_deleted_user_hidden_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)

    assert_not_contains(response, text_attachment.name)
    assert_not_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_deleted_user_hidden_post_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_user_hidden_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user, is_hidden=True
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)

    assert_not_contains(response, text_attachment.name)
    assert_not_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_other_user_hidden_post_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread,
        original=get_random_string(12),
        poster=other_user,
        is_hidden=True,
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)

    assert_not_contains(response, text_attachment.name)
    assert_not_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_hidden_post_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    user,
    text_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user, is_hidden=True
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_post_with_all_attachment_types_embedded(
    thread_reply_factory,
    user_client,
    user_private_thread,
    text_attachment,
    image_attachment,
    image_thumbnail_attachment,
    video_attachment,
    broken_text_attachment,
    broken_image_attachment,
    broken_image_thumbnail_attachment,
    broken_video_attachment,
    user_text_attachment,
    user_image_attachment,
    user_image_thumbnail_attachment,
    user_video_attachment,
    user_broken_text_attachment,
    user_broken_image_attachment,
    user_broken_image_thumbnail_attachment,
    user_broken_video_attachment,
    other_user_text_attachment,
    other_user_image_attachment,
    other_user_image_thumbnail_attachment,
    other_user_video_attachment,
    other_user_broken_text_attachment,
    other_user_broken_image_attachment,
    other_user_broken_image_thumbnail_attachment,
    other_user_broken_video_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    text_attachment.associate_with_post(post)
    text_attachment.save()

    image_attachment.associate_with_post(post)
    image_attachment.save()

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    video_attachment.associate_with_post(post)
    video_attachment.save()

    broken_text_attachment.associate_with_post(post)
    broken_text_attachment.save()

    broken_image_attachment.associate_with_post(post)
    broken_image_attachment.save()

    broken_image_thumbnail_attachment.associate_with_post(post)
    broken_image_thumbnail_attachment.save()

    broken_video_attachment.associate_with_post(post)
    broken_video_attachment.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    user_image_thumbnail_attachment.associate_with_post(post)
    user_image_thumbnail_attachment.save()

    user_video_attachment.associate_with_post(post)
    user_video_attachment.save()

    user_broken_text_attachment.associate_with_post(post)
    user_broken_text_attachment.save()

    user_broken_image_attachment.associate_with_post(post)
    user_broken_image_attachment.save()

    user_broken_image_thumbnail_attachment.associate_with_post(post)
    user_broken_image_thumbnail_attachment.save()

    user_broken_video_attachment.associate_with_post(post)
    user_broken_video_attachment.save()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    other_user_image_attachment.associate_with_post(post)
    other_user_image_attachment.save()

    other_user_image_thumbnail_attachment.associate_with_post(post)
    other_user_image_thumbnail_attachment.save()

    other_user_video_attachment.associate_with_post(post)
    other_user_video_attachment.save()

    other_user_broken_text_attachment.associate_with_post(post)
    other_user_broken_text_attachment.save()

    other_user_broken_image_attachment.associate_with_post(post)
    other_user_broken_image_attachment.save()

    other_user_broken_image_thumbnail_attachment.associate_with_post(post)
    other_user_broken_image_thumbnail_attachment.save()

    other_user_broken_video_attachment.associate_with_post(post)
    other_user_broken_video_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{text_attachment.id}" name="{text_attachment.name}" slug="{text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{image_thumbnail_attachment.id}" name="{image_thumbnail_attachment.name}" slug="{image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{video_attachment.id}" name="{video_attachment.name}" slug="{video_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{broken_text_attachment.id}" name="{broken_text_attachment.name}" slug="{broken_text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{broken_image_attachment.id}" name="{broken_image_attachment.name}" slug="{broken_image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{broken_image_thumbnail_attachment.id}" name="{broken_image_thumbnail_attachment.name}" slug="{broken_image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{broken_video_attachment.id}" name="{broken_video_attachment.name}" slug="{broken_video_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_text_attachment.id}" name="{user_text_attachment.name}" slug="{user_text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_image_attachment.id}" name="{user_image_attachment.name}" slug="{user_image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_image_thumbnail_attachment.id}" name="{user_image_thumbnail_attachment.name}" slug="{user_image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_video_attachment.id}" name="{user_video_attachment.name}" slug="{user_video_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_broken_text_attachment.id}" name="{user_broken_text_attachment.name}" slug="{user_broken_text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_broken_image_attachment.id}" name="{user_broken_image_attachment.name}" slug="{user_broken_image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_broken_image_thumbnail_attachment.id}" name="{user_broken_image_thumbnail_attachment.name}" slug="{user_broken_image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{user_broken_video_attachment.id}" name="{user_broken_video_attachment.name}" slug="{user_broken_video_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_text_attachment.id}" name="{other_user_text_attachment.name}" slug="{other_user_text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_image_attachment.id}" name="{other_user_image_attachment.name}" slug="{other_user_image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_image_thumbnail_attachment.id}" name="{other_user_image_thumbnail_attachment.name}" slug="{other_user_image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_video_attachment.id}" name="{other_user_video_attachment.name}" slug="{other_user_video_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_broken_text_attachment.id}" name="{other_user_broken_text_attachment.name}" slug="{other_user_broken_text_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_broken_image_attachment.id}" name="{other_user_broken_image_attachment.name}" slug="{other_user_broken_image_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_broken_image_thumbnail_attachment.id}" name="{other_user_broken_image_thumbnail_attachment.name}" slug="{other_user_broken_image_thumbnail_attachment.slug}">'
        "\n"
        f'<misago-attachment id="{other_user_broken_video_attachment.id}" name="{other_user_broken_video_attachment.name}" slug="{other_user_broken_video_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [
            text_attachment.id,
            image_attachment.id,
            image_thumbnail_attachment.id,
            video_attachment.id,
            broken_text_attachment.id,
            broken_image_attachment.id,
            broken_image_thumbnail_attachment.id,
            broken_video_attachment.id,
            user_text_attachment.id,
            user_image_attachment.id,
            user_image_thumbnail_attachment.id,
            user_video_attachment.id,
            user_broken_text_attachment.id,
            user_broken_image_attachment.id,
            user_broken_image_thumbnail_attachment.id,
            user_broken_video_attachment.id,
            other_user_text_attachment.id,
            other_user_image_attachment.id,
            other_user_image_thumbnail_attachment.id,
            other_user_video_attachment.id,
            other_user_broken_text_attachment.id,
            other_user_broken_image_attachment.id,
            other_user_broken_image_thumbnail_attachment.id,
            other_user_broken_video_attachment.id,
        ],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, text_attachment.name)
    assert_contains(response, text_attachment.get_absolute_url())

    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())

    assert_contains(response, image_thumbnail_attachment.name)
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, video_attachment.name)
    assert_contains(response, video_attachment.get_absolute_url())

    assert_contains(response, broken_text_attachment.name)
    assert_not_contains(response, broken_text_attachment.get_absolute_url())

    assert_contains(response, broken_image_attachment.name)
    assert_not_contains(response, broken_image_attachment.get_absolute_url())

    assert_contains(response, broken_image_thumbnail_attachment.name)
    assert_not_contains(response, broken_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, broken_video_attachment.name)
    assert_not_contains(response, broken_video_attachment.get_absolute_url())

    assert_contains(response, user_text_attachment.name)
    assert_contains(response, user_text_attachment.get_absolute_url())

    assert_contains(response, user_image_attachment.name)
    assert_contains(response, user_image_attachment.get_absolute_url())

    assert_contains(response, user_image_thumbnail_attachment.name)
    assert_contains(response, user_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, user_video_attachment.name)
    assert_contains(response, user_video_attachment.get_absolute_url())

    assert_contains(response, user_broken_text_attachment.name)
    assert_not_contains(response, user_broken_text_attachment.get_absolute_url())

    assert_contains(response, user_broken_image_attachment.name)
    assert_not_contains(response, user_broken_image_attachment.get_absolute_url())

    assert_contains(response, user_broken_image_thumbnail_attachment.name)
    assert_not_contains(
        response, user_broken_image_thumbnail_attachment.get_absolute_url()
    )

    assert_contains(response, user_broken_video_attachment.name)
    assert_not_contains(response, user_broken_video_attachment.get_absolute_url())

    assert_contains(response, other_user_text_attachment.name)
    assert_contains(response, other_user_text_attachment.get_absolute_url())

    assert_contains(response, other_user_image_attachment.name)
    assert_contains(response, other_user_image_attachment.get_absolute_url())

    assert_contains(response, other_user_image_thumbnail_attachment.name)
    assert_contains(response, other_user_image_thumbnail_attachment.get_absolute_url())

    assert_contains(response, other_user_video_attachment.name)
    assert_contains(response, other_user_video_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_text_attachment.name)
    assert_not_contains(response, other_user_broken_text_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_image_attachment.name)
    assert_not_contains(response, other_user_broken_image_attachment.get_absolute_url())

    assert_contains(response, other_user_broken_image_thumbnail_attachment.name)
    assert_not_contains(
        response, other_user_broken_image_thumbnail_attachment.get_absolute_url()
    )

    assert_contains(response, other_user_broken_video_attachment.name)
    assert_not_contains(response, other_user_broken_video_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_deleted_user_post_embedded_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    image_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    image_attachment.associate_with_post(post)
    image_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_deleted_user_post_embedded_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    image_attachment,
):
    post = thread_reply_factory(user_private_thread, original=get_random_string(12))

    image_attachment.associate_with_post(post)
    image_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_post_embedded_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    image_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    image_attachment.associate_with_post(post)
    image_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_other_user_post_embedded_attachments_to_user(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_user,
    image_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=other_user
    )

    image_attachment.associate_with_post(post)
    image_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_post_embedded_attachments_to_moderator(
    thread_reply_factory,
    moderator_client,
    user_private_thread,
    user,
    image_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    image_attachment.associate_with_post(post)
    image_attachment.save()

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_post_embedded_attachments_from_other_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12)
    )

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_post_embedded_attachments_from_hidden_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
    )

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    # TODO: fix this in #2002
    assert_not_contains(
        response, "You can&#x27;t download attachments in this category."
    )

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_post_embedded_attachments_from_post_on_other_page(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12)
    )

    for _ in range(5):
        thread_reply_factory(user_private_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(
        response, "You can&#x27;t download attachments in this category."
    )

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_post_embedded_attachments_from_other_thread_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_post_embedded_attachments_from_inaccessible_other_thread(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
    image_attachment,
):
    other_thread.is_hidden = True
    other_thread.save()

    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_post_embedded_attachments_from_inaccessible_other_thread_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(
        other_thread, original=get_random_string(12), is_unapproved=True
    )

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_post_embedded_attachments_from_other_category(
    thread_factory,
    thread_reply_factory,
    user_client,
    members_group,
    sibling_category,
    user_private_thread,
    user,
    image_attachment,
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.ATTACHMENTS,
    )

    other_thread = thread_factory(sibling_category)
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_post_embedded_attachments_from_other_category_without_attachments_permission(
    thread_factory,
    thread_reply_factory,
    user_client,
    members_group,
    sibling_category,
    user_private_thread,
    user,
    image_attachment,
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )

    other_thread = thread_factory(sibling_category)
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_not_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_post_embedded_attachments_from_private_thread_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_user_private_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(
        other_user_private_thread, original=get_random_string(12)
    )

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_doesnt_show_post_embedded_attachments_from_inaccessible_private_thread_post(
    thread_reply_factory,
    user_client,
    user_private_thread,
    private_thread,
    user,
    image_attachment,
):
    other_post = thread_reply_factory(private_thread, original=get_random_string(12))

    image_attachment.associate_with_post(other_post)
    image_attachment.save()

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_doesnt_show_unassociated_embedded_attachment(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    image_attachment,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed += (
        "\n"
        f'<misago-attachment id="{image_attachment.id}" name="{image_attachment.name}" slug="{image_attachment.slug}">'
    )
    post.metadata = {
        "attachments": [image_attachment.id],
    }
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-attachment")

    assert_not_contains(response, "rich-text-image")
    assert_contains(response, image_attachment.name)
    assert_contains(response, image_attachment.get_absolute_url())


def test_private_thread_detail_view_shows_user_own_post_edits_to_user(
    thread_reply_factory,
    user_client,
    user,
    user_private_thread,
):
    post = thread_reply_factory(user_private_thread, poster=user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_user_own_post_edits_to_user_without_edits_history_permission(
    thread_reply_factory,
    user_client,
    user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_user_own_post_edits_to_user_without_edits_permission(
    thread_reply_factory,
    user_client,
    user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_other_user_post_edits_to_user(
    thread_reply_factory,
    user_client,
    other_user,
    user_private_thread,
):
    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_other_user_post_edits_to_user_without_edits_history_permission(
    thread_reply_factory,
    user_client,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_other_user_post_edits_to_user_without_edits_permission(
    thread_reply_factory,
    user_client,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Edited 17 times.")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_other_user_post_last_edit_data_to_user(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    user_private_thread,
):
    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(response, f"Last by {user.username},")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_other_user_post_last_edit_data_to_user_without_edits_history_permission(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_not_contains(response, f"Last by {user.username},")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_other_user_post_last_edit_data_to_user_without_permission(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Edited 17 times.")
    assert_not_contains(response, f"Last by {user.username},")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_other_user_post_last_edit_reason_to_user(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    user_private_thread,
):
    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.last_edit_reason = "edited out typos"
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_contains(response, f"Last by {user.username},")
    assert_contains(response, "Reason: edited out typos")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_other_user_post_last_edit_reason_to_user_without_edits_history_permission(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.COUNT
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.last_edit_reason = "edited out typos"
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Edited 17 times.")
    assert_not_contains(response, f"Last by {user.username},")
    assert_not_contains(response, "Reason: edited out typos")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_other_user_post_last_edit_reason_to_user_without_permission(
    thread_reply_factory,
    user_client,
    user,
    other_user,
    members_group,
    user_private_thread,
):
    members_group.can_see_others_post_edits = CanSeePostEdits.NEVER
    members_group.save()

    post = thread_reply_factory(user_private_thread, poster=other_user, edits=17)
    post.updated_at = timezone.now()
    post.last_editor = user
    post.last_editor_name = user.username
    post.last_editor_slug = user.slug
    post.last_edit_reason = "edited out typos"
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Edited 17 times.")
    assert_not_contains(response, f"Last by {user.username},")
    assert_not_contains(response, "Reason: edited out typos")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-edits",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_post_with_deleted_user_like_to_user(
    thread_reply_factory,
    user_client,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "DeletedUser likes this")


def test_private_thread_detail_view_shows_post_with_other_user_like_to_user(
    thread_reply_factory,
    user_client,
    other_user,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, f"{other_user.username} likes this")


def test_private_thread_detail_view_shows_post_with_user_like_to_user(
    thread_reply_factory,
    user_client,
    user,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")


def test_private_thread_detail_view_shows_post_with_user_like_to_user_without_own_posts_last_likes_permission(
    thread_reply_factory,
    user_client,
    members_group,
    user,
    other_user,
    other_user_private_thread,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)
    like_post(post, user)
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")
    assert_contains(response, f"You and 1 other like this")
    assert_not_contains(response, f"You and {other_user.username} like this")


def test_private_thread_detail_view_shows_post_with_user_like_to_user_without_own_posts_likes_permission(
    thread_reply_factory,
    user_client,
    members_group,
    user,
    other_user,
    other_user_private_thread,
):
    members_group.can_see_own_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    post = thread_reply_factory(other_user_private_thread, poster=user)
    like_post(post, user)
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")
    assert_not_contains(response, "You and 1 other like this")
    assert_not_contains(response, f"You and {other_user.username} like this")


def test_private_thread_detail_view_shows_post_with_other_user_like_to_user_without_others_posts_last_likes_permission(
    thread_reply_factory,
    members_group,
    user_client,
    other_user,
    other_user_private_thread,
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Liked")
    assert_contains(response, "1 other likes this")
    assert_not_contains(response, f"{other_user.username} likes this")


def test_private_thread_detail_view_shows_post_with_other_user_like_to_user_without_others_posts_likes_permission(
    thread_reply_factory,
    members_group,
    user_client,
    other_user,
    other_user_private_thread,
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)
    like_post(post, other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Liked")
    assert_not_contains(response, "1 other likes this")
    assert_not_contains(response, f"{other_user.username} likes this")


def test_private_thread_detail_view_show_like_button_to_user_with_permission(
    thread_reply_factory,
    user_client,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Like")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-like",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_like_button_to_user_without_permission(
    thread_reply_factory,
    members_group,
    user_client,
    other_user_private_thread,
):
    members_group.can_like_posts = False
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(response, "Like")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-like",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_like_button_to_user_with_permission_for_liked_post(
    thread_reply_factory,
    user_client,
    user,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-like",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_unlike_button_to_user_with_permission_for_liked_post(
    thread_reply_factory,
    user_client,
    user,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_unlike_button_to_user_without_permission_for_liked_post(
    thread_reply_factory,
    members_group,
    user_client,
    user,
    other_user_private_thread,
):
    members_group.can_like_posts = False
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)
    like_post(post, user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Liked")
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-unlike",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_post_likes_link_for_post_without_likes(
    thread_reply_factory,
    user_client,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_post_likes_link_for_post_with_likes(
    thread_reply_factory,
    user_client,
    other_user_private_thread,
):
    post = thread_reply_factory(other_user_private_thread)
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(
        response,
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_post_likes_link_for_post_with_likes_for_user_without_last_likes_permission(
    thread_reply_factory,
    user_client,
    members_group,
    other_user_private_thread,
):
    members_group.can_see_others_post_likes = CanSeePostLikes.COUNT
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_doesnt_show_post_likes_link_for_post_with_likes_for_user_without_likes_permission(
    thread_reply_factory,
    user_client,
    members_group,
    other_user_private_thread,
):
    members_group.can_see_others_post_likes = CanSeePostLikes.NEVER
    members_group.save()

    post = thread_reply_factory(other_user_private_thread)
    like_post(post, "DeletedUser")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_not_contains(
        response,
        reverse(
            "misago:private-thread-post-likes",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "post_id": post.id,
            },
        ),
    )


def test_private_thread_detail_view_shows_post_with_previous_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
):
    previous_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12)
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{previous_post.poster}" post="{previous_post.id}">'
        f"{previous_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [previous_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_hidden_previous_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
):
    previous_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), is_hidden=True
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{previous_post.poster}" post="{previous_post.id}">'
        f"{previous_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [previous_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_post_with_quote_of_deleted_user_post_from_other_page(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
):
    previous_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12)
    )

    for _ in range(5):
        thread_reply_factory(user_private_thread, original=get_random_string(12))

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{previous_post.poster}" post="{previous_post.id}">'
        f"{previous_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [previous_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_post_with_quote_of_user_post_from_other_page(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
):
    previous_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    for _ in range(5):
        thread_reply_factory(user_private_thread, original=get_random_string(12))

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{previous_post.poster}" post="{previous_post.id}">'
        f"{previous_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [previous_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_shows_post_with_quote_of_other_user_post_from_other_page(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
    other_user,
):
    previous_post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=other_user
    )

    for _ in range(5):
        thread_reply_factory(user_private_thread, original=get_random_string(12))

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{previous_post.poster}" post="{previous_post.id}">'
        f"{previous_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [previous_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
                "page": 2,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_other_thread_deleted_user_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
):
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_other_thread_user_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
):
    other_post = thread_reply_factory(
        other_thread, original=get_random_string(12), poster=user
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_other_thread_other_user_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
    other_user,
):
    other_post = thread_reply_factory(
        other_thread, original=get_random_string(12), poster=other_user
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_inaccessible_thread_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
):
    other_thread.is_hidden = True
    other_thread.save()

    other_post = thread_reply_factory(other_thread, original=get_random_string(12))
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_inaccessible_thread_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_thread,
    user,
):
    other_post = thread_reply_factory(
        other_thread, original=get_random_string(12), is_unapproved=True
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_other_category_post_quote(
    thread_factory,
    thread_reply_factory,
    user_client,
    members_group,
    sibling_category,
    user_private_thread,
    user,
):
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.SEE,
    )
    CategoryGroupPermission.objects.create(
        category=sibling_category,
        group=members_group,
        permission=CategoryPermission.BROWSE,
    )

    other_thread = thread_factory(sibling_category)
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_other_category_inaccessible_post_quote(
    thread_factory,
    thread_reply_factory,
    user_client,
    sibling_category,
    user_private_thread,
    user,
):
    other_thread = thread_factory(sibling_category)
    other_post = thread_reply_factory(other_thread, original=get_random_string(12))

    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_private_thread_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    other_user_private_thread,
    user,
):
    other_post = thread_reply_factory(
        other_user_private_thread, original=get_random_string(12)
    )
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_inaccessible_private_thread_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    private_thread,
    user,
):
    other_post = thread_reply_factory(private_thread, original=get_random_string(12))
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="{other_post.poster}" post="{other_post.id}">'
        f"{other_post.parsed}"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [other_post.id]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")


def test_private_thread_detail_view_shows_post_with_deleted_post_quote(
    thread_reply_factory,
    user_client,
    user_private_thread,
    user,
):
    post = thread_reply_factory(
        user_private_thread, original=get_random_string(12), poster=user
    )

    post.parsed = (
        f'<misago-quote user="Poster" post="{post.id + 100}">'
        "<p>Lorem ipsum</p>"
        "</misago-quote>"
        "\n"
        f"{post.parsed}"
    )
    post.metadata = {"posts": [post.id + 100]}
    post.save()

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": user_private_thread.id,
                "slug": user_private_thread.slug,
            },
        )
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)

    assert_not_contains(response, "<misago-quote")
    assert_contains(response, "rich-text-quote-btn")
