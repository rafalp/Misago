import pytest
from django.urls import reverse

from ...permissions.proxy import UserPermissionsProxy
from ..postsfeed import PostsFeed, PrivateThreadPostsFeed, ThreadPostsFeed
from ..test import reply_thread


@pytest.fixture
def request_factory(rf, dynamic_settings, cache_versions):
    def factory(user):
        request = rf.get("/")
        request.settings = dynamic_settings
        request.user = user
        request.user_permissions = UserPermissionsProxy(user, cache_versions)
        return request

    return factory


def test_posts_feed_returns_post_data(request_factory, user, thread, post):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post])
    feed_data = posts_feed.get_context_data()

    assert feed_data["template_name"] == posts_feed.template_name
    assert feed_data["items"][0]["template_name"] == posts_feed.post_template_name
    assert feed_data["items"][0]["post"] == post


def test_posts_feed_sets_posters_in_post_data(
    request_factory, user, other_user, thread, other_user_reply
):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [other_user_reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == other_user_reply
    assert post_data["poster"] == other_user
    assert post_data["poster_name"] == other_user.username


def test_posts_feed_sets_rich_text_data_in_post_data(
    request_factory, user, thread, other_user_reply, text_attachment
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    other_user_reply.metadata = {"attachments": [text_attachment.id]}
    other_user_reply.save()

    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [other_user_reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["rich_text_data"]["attachment_errors"] == {}
    assert post_data["rich_text_data"]["attachments"] == {
        text_attachment.id: text_attachment
    }


def test_posts_feed_marks_post_as_animated(request_factory, user, thread, post, reply):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post, reply])
    posts_feed.set_animated_posts([post.id])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == post
    assert post_data["animate"]

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["animate"]


def test_posts_feed_marks_post_as_unread(request_factory, user, thread, post, reply):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post, reply])
    posts_feed.set_unread_posts([post.id])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == post
    assert post_data["unread"]

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["unread"]


def test_thread_posts_feed_marks_post_as_editable(
    request_factory, user, thread, user_reply, reply
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, thread, [user_reply, reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": thread.id,
            "slug": thread.slug,
            "post": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_thread_posts_feed_marks_original_post_as_editable(
    request_factory, user, user_thread, reply
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, user_thread, [user_thread.first_post, reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
            "post": user_thread.first_post.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_thread_posts_feed_marks_original_post_as_thread_editable(
    request_factory, user, user_thread, reply
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, user_thread, [user_thread.first_post, reply])
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_thread_posts_feed_marks_post_as_editable_by_moderator(
    request_factory, moderator, thread, user_reply, reply
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, thread, [user_reply, reply])
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": thread.id,
            "slug": thread.slug,
            "post": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": thread.id,
            "slug": thread.slug,
            "post": reply.id,
        },
    )


def test_thread_posts_feed_marks_original_post_as_editable_by_moderator(
    request_factory, moderator, user_thread, reply
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, user_thread, [user_thread.first_post, reply])
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
            "post": reply.id,
        },
    )


def test_thread_posts_feed_marks_original_post_as_thread_editable_by_moderator(
    request_factory, moderator, user_thread, reply
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, user_thread, [user_thread.first_post, reply])
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-thread",
        kwargs={
            "id": user_thread.id,
            "slug": user_thread.slug,
            "post": reply.id,
        },
    )


def test_private_thread_posts_feed_marks_post_as_editable(
    request_factory, user, user_private_thread
):
    user_reply = reply_thread(user_private_thread, user)
    reply = reply_thread(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_reply, reply]
    )
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_posts_feed_marks_original_post_as_editable(
    request_factory, user, user_private_thread
):
    reply = reply_thread(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": user_private_thread.first_post.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_posts_feed_marks_original_post_as_thread_editable(
    request_factory, user, user_private_thread
):
    reply = reply_thread(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["edit_url"]


def test_private_thread_posts_feed_marks_post_as_editable_by_moderator(
    request_factory, moderator, user, user_private_thread
):
    user_reply = reply_thread(user_private_thread, user)
    reply = reply_thread(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_reply, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": reply.id,
        },
    )


def test_private_thread_posts_feed_marks_original_post_as_editable_by_moderator(
    request_factory, moderator, user_private_thread
):
    reply = reply_thread(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": reply.id,
        },
    )


def test_private_thread_posts_feed_marks_original_post_as_thread_editable_by_moderator(
    request_factory, moderator, user_private_thread
):
    reply = reply_thread(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_private_thread.first_post
    assert post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:edit-private-thread",
        kwargs={
            "id": user_private_thread.id,
            "slug": user_private_thread.slug,
            "post": reply.id,
        },
    )
