import pytest
from django.urls import reverse

from ..postfeed import PrivateThreadPostFeed


@pytest.fixture
def request_factory(rf, user_permissions_factory, dynamic_settings):
    def factory(user):
        request = rf.get("/")
        request.settings = dynamic_settings
        request.user = user
        request.user_permissions = user_permissions_factory(user)
        return request

    return factory


def test_private_thread_post_feed_marks_post_as_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    user_reply = thread_reply_factory(user_private_thread, poster=user)
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    post_feed = PrivateThreadPostFeed(request, user_private_thread, [user_reply, reply])
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_post_feed_marks_original_post_as_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    post_feed = PrivateThreadPostFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": user_private_thread.first_post.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_post_feed_marks_original_post_as_thread_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    post_feed = PrivateThreadPostFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    post_feed.set_allow_edit_thread(True)
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_post_feed_marks_post_as_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user, user_private_thread
):
    user_reply = thread_reply_factory(user_private_thread, poster=user)
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    post_feed = PrivateThreadPostFeed(request, user_private_thread, [user_reply, reply])
    post_feed.set_allow_edit_thread(True)
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": reply.id,
        },
    )


def test_private_thread_post_feed_marks_original_post_as_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    post_feed = PrivateThreadPostFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    post_feed.set_allow_edit_thread(True)
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": reply.id,
        },
    )


def test_private_thread_post_feed_marks_original_post_as_thread_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    post_feed = PrivateThreadPostFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    post_feed.set_allow_edit_thread(True)
    feed_data = post_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:private-thread-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:private-thread-post-edit",
        kwargs={
            "thread_id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post_id": reply.id,
        },
    )
