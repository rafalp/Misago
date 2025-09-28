from django.utils.crypto import get_random_string
from django.urls import reverse

from ...conf.test import override_dynamic_settings
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


def test_thread_detail_view_shows_deleted_user_post_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12))
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_post_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12))
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_post_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12))
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_user_post_to_anonymous_user(
    thread_reply_factory, client, thread, user
):
    post = thread_reply_factory(thread, original=get_random_string(12), poster=user)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_user_post_to_user(
    thread_reply_factory, user_client, thread, user
):
    post = thread_reply_factory(thread, original=get_random_string(12), poster=user)
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_other_user_post_to_user(
    thread_reply_factory, user_client, thread, other_user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=other_user
    )
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_user_post_to_moderator(
    thread_reply_factory, moderator_client, thread, user
):
    post = thread_reply_factory(thread, original=get_random_string(12), poster=user)
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_doesnt_show_unapproved_post_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), is_unapproved=True
    )
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_doesnt_show_unapproved_post_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), is_unapproved=True
    )
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_not_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_shows_unapproved_post_to_poster(
    thread_reply_factory, user_client, thread, user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=user, is_unapproved=True
    )
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_unapproved_post_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), is_unapproved=True
    )
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_user_unapproved_post_to_moderator(
    thread_reply_factory, moderator_client, thread, user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=user, is_unapproved=True
    )
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_hidden_post_to_anonymous_user(
    thread_reply_factory, client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12), is_hidden=True)
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_hidden_post_to_user(
    thread_reply_factory, user_client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12), is_hidden=True)
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_shows_deleted_user_hidden_post_to_moderator(
    thread_reply_factory, moderator_client, thread
):
    post = thread_reply_factory(thread, original=get_random_string(12), is_hidden=True)
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_user_hidden_post_to_anonymous_user(
    thread_reply_factory, client, thread, user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=user, is_hidden=True
    )
    response = client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_shows_user_hidden_post_to_user(
    thread_reply_factory, user_client, thread, user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=user, is_hidden=True
    )
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


def test_thread_detail_view_shows_other_user_hidden_post_to_user(
    thread_reply_factory, user_client, thread, other_user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=other_user, is_hidden=True
    )
    response = user_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_not_contains(response, post.original)


def test_thread_detail_view_shows_user_hidden_post_to_moderator(
    thread_reply_factory, moderator_client, thread, user
):
    post = thread_reply_factory(
        thread, original=get_random_string(12), poster=user, is_hidden=True
    )
    response = moderator_client.get(
        reverse("misago:thread", kwargs={"thread_id": thread.id, "slug": thread.slug})
    )
    assert_contains(response, post.get_absolute_url())
    assert_contains(response, post.original)


# TODO
# - hidden posts visibility tests
# - post attachments
# - post attachments without download permission
# - post embedded attachments
# - post attachments without download permission
# - post with other post quote
# - post with other thread quote
