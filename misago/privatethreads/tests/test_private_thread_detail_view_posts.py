from django.urls import reverse

from ...conf.test import override_dynamic_settings
from ...test import assert_contains, assert_not_contains


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_returns_redirect_to_first_page_if_page_is_out_of_range(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_returns_redirect_to_last_page_if_page_is_out_of_range(
    thread_reply_factory, user_client, other_user_private_thread
):
    for i in range(1, 20):
        thread_reply_factory(other_user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 123,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
            "page": 3,
        },
    )


def test_private_thread_detail_view_returns_redirect_if_explicit_first_page_is_given(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 1,
            },
        )
    )
    assert response.status_code == 302
    assert response["location"] == reverse(
        "misago:private-thread",
        kwargs={
            "thread_id": other_user_private_thread.id,
            "slug": other_user_private_thread.slug,
        },
    )


def test_private_thread_detail_view_ignores_explicit_first_page_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
                "page": 1,
            },
        ),
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_first_page_in_multi_page_thread(
    thread_reply_factory, user_client, other_user_private_thread
):
    for i in range(1, 7):
        thread_reply_factory(other_user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
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
def test_private_thread_detail_view_displays_middle_page_in_multi_page_thread(
    thread_reply_factory, user_client, other_user_private_thread
):
    for i in range(1, 12):
        thread_reply_factory(other_user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
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
def test_private_thread_detail_view_displays_last_page_in_multi_page_thread(
    thread_reply_factory, user_client, other_user_private_thread
):
    for i in range(1, 7):
        thread_reply_factory(other_user_private_thread, original=f"Reply no. {i}")

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
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


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_user_post(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_other_user_post(
    thread_reply_factory, user_client, other_user, other_user_private_thread
):
    post = thread_reply_factory(other_user_private_thread, poster=other_user)

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_deleted_user_post(
    thread_reply_factory, user_client, other_user_private_thread
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

    assert_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_user_hidden_post_with_content(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread, poster=user, original="Hidden post", is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_other_user_hidden_post_without_content(
    thread_reply_factory, user_client, other_user, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster=other_user,
        original="Hidden post",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_deleted_user_hidden_post_without_content(
    thread_reply_factory, user_client, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread, original="Hidden post", is_hidden=True
    )

    response = user_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_not_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_other_user_hidden_post_content_to_moderator(
    thread_reply_factory, moderator_client, other_user, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster=other_user,
        original="Hidden post",
        is_hidden=True,
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


@override_dynamic_settings(posts_per_page=5, posts_per_page_orphans=1)
def test_private_thread_detail_view_displays_deleted_user_hidden_post_content_to_moderator(
    thread_reply_factory, moderator_client, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread, original="Hidden post", is_hidden=True
    )

    response = moderator_client.get(
        reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )

    assert_contains(response, post.parsed)


# TODO:
# - post with attachments
# - hidden post with attachments
# - unapproved post
# - unapproved post with attachments
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
