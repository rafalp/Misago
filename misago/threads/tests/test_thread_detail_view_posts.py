from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...permissions.models import Moderator
from ...test import assert_contains, assert_not_contains


def test_thread_detail_view_returns_redirect_to_first_page_if_page_is_out_of_range(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
        },
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_thread_detail_view_returns_redirect_to_last_page_if_page_is_out_of_range(
    thread_reply_factory, user_client, thread
):
    for i in range(1, 20):
        thread_reply_factory(thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "page": 4,
        },
    )


def test_thread_detail_view_returns_redirect_if_explicit_first_page_is_given(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "page": 1,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:thread",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
        },
    )


def test_thread_detail_view_ignores_explicit_first_page_in_htmx(user_client, thread):
    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
                "page": 1,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_thread_detail_view_shows_first_page_in_multi_page_thread(
    thread_reply_factory, user_client, thread
):
    for i in range(1, 7):
        thread_reply_factory(thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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
def test_thread_detail_view_shows_middle_page_in_multi_page_thread(
    thread_reply_factory, user_client, thread
):
    for i in range(1, 12):
        thread_reply_factory(thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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
def test_thread_detail_view_shows_last_page_in_multi_page_thread(
    thread_reply_factory, user_client, thread
):
    for i in range(1, 7):
        thread_reply_factory(thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
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


def test_thread_detail_view_shows_user_post(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_other_user_post(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_deleted_user_post(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread)

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_user_unapproved_post_to_user(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(
        thread,
        original="Unapproved post",
        poster=user,
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_doesnt_show_other_user_unapproved_post_to_user(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(
        thread,
        original="Unapproved post",
        poster=other_user,
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


def test_thread_detail_view_doesnt_show_deleted_user_unapproved_post_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(
        thread,
        original="Unapproved post",
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


def test_thread_detail_view_shows_other_user_unapproved_post_to_category_moderator(
    thread_reply_factory, user_client, user, other_user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    post = thread_reply_factory(
        thread,
        original="Unapproved post",
        poster=other_user,
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_doesnt_show_deleted_user_unapproved_post_to_category_moderator(
    thread_reply_factory, user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    post = thread_reply_factory(
        thread,
        original="Unapproved post",
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_user_hidden_post_with_content(
    thread_reply_factory, user_client, user, thread
):
    post = thread_reply_factory(
        thread,
        poster=user,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_other_user_hidden_post_without_content(
    thread_reply_factory, user_client, other_user, thread
):
    post = thread_reply_factory(
        thread,
        poster=other_user,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


def test_thread_detail_view_shows_deleted_user_hidden_post_without_content(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(
        thread,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


def test_thread_detail_view_shows_other_user_hidden_post_content_to_category_moderator(
    thread_reply_factory, user_client, user, other_user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    post = thread_reply_factory(
        thread,
        poster=other_user,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_deleted_user_hidden_post_content_to_category_moderator(
    thread_reply_factory, user_client, user, thread
):
    Moderator.objects.create(
        user=user,
        is_global=False,
        categories=[thread.category_id],
    )

    post = thread_reply_factory(
        thread,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_other_user_hidden_post_content_to_global_moderator(
    thread_reply_factory, moderator_client, other_user, thread
):
    post = thread_reply_factory(
        thread,
        poster=other_user,
        original="Hidden post",
        is_hidden=True,
    )

    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_deleted_user_hidden_post_content_to_global_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(
        thread,
        original="Hidden post",
        is_hidden=True,
    )

    response = moderator_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


def test_thread_detail_view_shows_user_post_with_user_file_attachment(
    thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_file_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_text_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_file_attachment(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_image_attachment(
    thread_reply_factory, user_client, user, thread, user_image_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_image_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_image_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_image_attachment.associate_with_post(post)
    other_user_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_image_attachment(
    thread_reply_factory, user_client, user, thread, image_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    image_attachment.associate_with_post(post)
    image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_image_thumbnail_attachment(
    thread_reply_factory, user_client, user, thread, user_image_thumbnail_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_image_thumbnail_attachment.associate_with_post(post)
    user_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_image_thumbnail_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_image_thumbnail_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_image_thumbnail_attachment.associate_with_post(post)
    other_user_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_image_thumbnail_attachment(
    thread_reply_factory, user_client, user, thread, image_thumbnail_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_video_attachment(
    thread_reply_factory, user_client, user, thread, user_video_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_video_attachment.associate_with_post(post)
    user_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_video_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_video_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_video_attachment.associate_with_post(post)
    other_user_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_video_attachment(
    thread_reply_factory, user_client, user, thread, video_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    video_attachment.associate_with_post(post)
    video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_broken_file_attachment(
    thread_reply_factory, user_client, user, thread, user_broken_text_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_broken_text_attachment.associate_with_post(post)
    user_broken_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_broken_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_broken_file_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_broken_text_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_broken_text_attachment.associate_with_post(post)
    other_user_broken_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_broken_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_broken_file_attachment(
    thread_reply_factory, user_client, user, thread, broken_text_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    broken_text_attachment.associate_with_post(post)
    broken_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, broken_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_broken_image_attachment(
    thread_reply_factory, user_client, user, thread, user_broken_image_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_broken_image_attachment.associate_with_post(post)
    user_broken_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_broken_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_broken_image_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_broken_image_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_broken_image_attachment.associate_with_post(post)
    other_user_broken_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_broken_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_broken_image_attachment(
    thread_reply_factory, user_client, user, thread, broken_image_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    broken_image_attachment.associate_with_post(post)
    broken_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, broken_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_broken_image_thumbnail_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    user_broken_image_thumbnail_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_broken_image_thumbnail_attachment.associate_with_post(post)
    user_broken_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_broken_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_broken_image_thumbnail_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_broken_image_thumbnail_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_broken_image_thumbnail_attachment.associate_with_post(post)
    other_user_broken_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(
        response, other_user_broken_image_thumbnail_attachment.get_absolute_url()
    )


def test_thread_detail_view_shows_user_post_with_deleted_user_broken_image_thumbnail_attachment(
    thread_reply_factory, user_client, user, thread, broken_image_thumbnail_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    broken_image_thumbnail_attachment.associate_with_post(post)
    broken_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, broken_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_user_broken_video_attachment(
    thread_reply_factory, user_client, user, thread, user_broken_video_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    user_broken_video_attachment.associate_with_post(post)
    user_broken_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, user_broken_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_other_user_broken_video_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_broken_video_attachment,
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    other_user_broken_video_attachment.associate_with_post(post)
    other_user_broken_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, other_user_broken_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_deleted_user_broken_video_attachment(
    thread_reply_factory, user_client, user, thread, broken_video_attachment
):
    post = thread_reply_factory(
        thread,
        original="Post with attachment",
        poster=user,
    )

    broken_video_attachment.associate_with_post(post)
    broken_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)
    assert_contains(response, broken_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_user_file_attachment(
    thread_reply_factory, user_client, user, thread, user_text_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{user_text_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [user_text_attachment.id]},
    )

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, user_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_other_user_file_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_text_attachment,
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{other_user_text_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [other_user_text_attachment.id]},
    )

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, other_user_text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_deleted_user_file_attachment(
    thread_reply_factory, user_client, user, thread, text_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{text_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [text_attachment.id]},
    )

    text_attachment.associate_with_post(post)
    text_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, text_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_user_image_attachment(
    thread_reply_factory, user_client, user, thread, user_image_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{user_image_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [user_image_attachment.id]},
    )

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, user_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_other_user_image_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_image_attachment,
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{other_user_image_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [other_user_image_attachment.id]},
    )

    other_user_image_attachment.associate_with_post(post)
    other_user_image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, other_user_image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_deleted_user_image_attachment(
    thread_reply_factory, user_client, user, thread, image_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{image_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [image_attachment.id]},
    )

    image_attachment.associate_with_post(post)
    image_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, image_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_user_image_thumbnail_attachment(
    thread_reply_factory, user_client, user, thread, user_image_thumbnail_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{user_image_thumbnail_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [user_image_thumbnail_attachment.id]},
    )

    user_image_thumbnail_attachment.associate_with_post(post)
    user_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, user_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_other_user_image_thumbnail_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_image_thumbnail_attachment,
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{other_user_image_thumbnail_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [other_user_image_thumbnail_attachment.id]},
    )

    other_user_image_thumbnail_attachment.associate_with_post(post)
    other_user_image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, other_user_image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_deleted_user_image_thumbnail_attachment(
    thread_reply_factory, user_client, user, thread, image_thumbnail_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{image_thumbnail_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [image_thumbnail_attachment.id]},
    )

    image_thumbnail_attachment.associate_with_post(post)
    image_thumbnail_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, image_thumbnail_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_user_video_attachment(
    thread_reply_factory, user_client, user, thread, user_video_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{user_video_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [user_video_attachment.id]},
    )

    user_video_attachment.associate_with_post(post)
    user_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, user_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_other_user_video_attachment(
    thread_reply_factory,
    user_client,
    user,
    thread,
    other_user_video_attachment,
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{other_user_video_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [other_user_video_attachment.id]},
    )

    other_user_video_attachment.associate_with_post(post)
    other_user_video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, other_user_video_attachment.get_absolute_url())


def test_thread_detail_view_shows_user_post_with_embedded_deleted_user_video_attachment(
    thread_reply_factory, user_client, user, thread, video_attachment
):
    post = thread_reply_factory(
        thread,
        parsed=(
            "<p>Attachment with post</p>"
            "\n"
            f'<misago-attachment id="{video_attachment.id}" '
            'name="attachment.txt" slug="attachment-txt">'
        ),
        poster=user,
        metadata={"attachments": [video_attachment.id]},
    )

    video_attachment.associate_with_post(post)
    video_attachment.save()

    response = user_client.get(
        reverse(
            "misago:thread",
            kwargs={
                "thread_id": thread.id,
                "slug": thread.slug,
            },
        )
    )

    assert_contains(response, "Attachment with post")
    assert_not_contains(response, "<misago-attachment")
    assert_contains(response, video_attachment.get_absolute_url())


# TODO:
# - other user post attachments
# - deleted user post attachments
# - user post attachments without attachments permission
# - other user post attachments without attachments permission
# - deleted user post attachments without attachments permission
# - embedded attachment from same post
# - embedded attachment from same user unapproved post
# - embedded attachment from same user hidden post
# - embedded attachment from other user post
# - embedded attachment from user user unapproved post
# - embedded attachment from other user hidden post
# - embedded attachment from deleted user post
# - embedded attachment from deleted user unapproved post
# - embedded attachment from deleted user hidden post
# - ditto
# - same thread user quote
# - same thread other user quote
# - same thread deleted user quote
# - accessible thread user quote
# - accessible thread other user quote
# - accessible thread deleted user quote
# - inaccessible thread user quote
# - inaccessible thread other user quote
# - inaccessible thread deleted user quote
# - accessible private thread user quote
# - accessible private thread other user quote
# - accessible private thread deleted user quote
# - inaccessible private thread user quote
# - inaccessible private thread other user quote
# - inaccessible private thread deleted user quote
