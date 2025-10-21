import pytest
from django.urls import reverse

from ...permissions.proxy import UserPermissionsProxy
from ..postsfeed import PostsFeed, PrivateThreadPostsFeed, ThreadPostsFeed


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
    assert post_data["attachments"] == []


def test_posts_feed_sets_extra_post_attachments(
    request_factory, user, thread, other_user_reply, text_attachment
):
    text_attachment.associate_with_post(other_user_reply)
    text_attachment.save()

    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [other_user_reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["rich_text_data"]["attachment_errors"] == {}
    assert post_data["rich_text_data"]["attachments"] == {
        text_attachment.id: text_attachment,
    }
    assert post_data["attachments"] == [text_attachment]


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


def test_posts_feed_marks_post_as_new(request_factory, user, thread, post, reply):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post, reply])
    posts_feed.set_unread_posts([post.id])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == post
    assert post_data["is_new"]

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert not other_post_data["is_new"]


def test_thread_posts_feed_marks_post_as_editable(
    request_factory, user, thread, user_reply, reply
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, thread, [user_reply, reply])
    feed_data = posts_feed.get_context_data()

    post_data = feed_data["items"][0]
    assert post_data["post"] == user_reply
    assert post_data["edit_url"] == reverse(
        "misago:thread-post-edit",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": user_reply.id,
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
        "misago:thread-post-edit",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
            "post_id": user_thread.first_post.id,
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
        "misago:thread-edit",
        kwargs={
            "thread_id": user_thread.id,
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
        "misago:thread-post-edit",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": user_reply.id,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:thread-post-edit",
        kwargs={
            "thread_id": thread.id,
            "slug": thread.slug,
            "post_id": reply.id,
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
        "misago:thread-edit",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:thread-post-edit",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
            "post_id": reply.id,
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
        "misago:thread-edit",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
        },
    )

    other_post_data = feed_data["items"][1]
    assert other_post_data["post"] == reply
    assert other_post_data["edit_url"] == reverse(
        "misago:thread-post-edit",
        kwargs={
            "thread_id": user_thread.id,
            "slug": user_thread.slug,
            "post_id": reply.id,
        },
    )


def test_private_thread_posts_feed_marks_post_as_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    user_reply = thread_reply_factory(user_private_thread, poster=user)
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_reply, reply]
    )
    feed_data = posts_feed.get_context_data()

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


def test_private_thread_posts_feed_marks_original_post_as_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    feed_data = posts_feed.get_context_data()

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


def test_private_thread_posts_feed_marks_original_post_as_thread_editable(
    request_factory, thread_reply_factory, user, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(user)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

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


def test_private_thread_posts_feed_marks_post_as_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user, user_private_thread
):
    user_reply = thread_reply_factory(user_private_thread, poster=user)
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_reply, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

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


def test_private_thread_posts_feed_marks_original_post_as_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

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


def test_private_thread_posts_feed_marks_original_post_as_thread_editable_by_moderator(
    request_factory, thread_reply_factory, moderator, user_private_thread
):
    reply = thread_reply_factory(user_private_thread)

    request = request_factory(moderator)

    posts_feed = PrivateThreadPostsFeed(
        request, user_private_thread, [user_private_thread.first_post, reply]
    )
    posts_feed.set_allow_edit_thread(True)
    feed_data = posts_feed.get_context_data()

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


def test_posts_feed_returns_thread_update_data(
    request_factory, user, thread, post, thread_update
):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["template_name"] == posts_feed.template_name
    assert (
        feed_data["items"][1]["template_name"] == posts_feed.thread_update_template_name
    )
    assert feed_data["items"][1]["thread_update"] == thread_update


def test_posts_feed_sets_actors_in_thread_update_data(
    request_factory, user, thread, post, thread_update
):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert feed_data["items"][1]["actor"] == user
    assert feed_data["items"][1]["actor_name"] == user.username


def test_posts_feed_sets_action_data_in_thread_update_data(
    request_factory, user, thread, post, thread_update
):
    request = request_factory(user)

    posts_feed = PostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert feed_data["items"][1]["icon"] == "lock_open"
    assert feed_data["items"][1]["description"] == "Opened thread"


def test_posts_feed_marks_thread_update_as_animated(
    request_factory, user, thread, post, thread_update, thread_update_context
):
    request = request_factory(user)

    posts_feed = PostsFeed(
        request, thread, [post], [thread_update, thread_update_context]
    )
    posts_feed.set_animated_thread_updates([thread_update_context.id])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert not feed_data["items"][1]["animate"]

    assert feed_data["items"][2]["thread_update"] == thread_update_context
    assert feed_data["items"][2]["animate"]


def test_posts_feed_marks_thread_update_as_animated(
    request_factory, user, thread, post, thread_update, thread_update_context
):
    request = request_factory(user)

    posts_feed = PostsFeed(
        request, thread, [post], [thread_update, thread_update_context]
    )
    posts_feed.set_animated_thread_updates([thread_update_context.id])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert not feed_data["items"][1]["animate"]

    assert feed_data["items"][2]["thread_update"] == thread_update_context
    assert feed_data["items"][2]["animate"]


def test_thread_posts_feed_doesnt_mark_thread_update_as_hidable_by_user(
    request_factory, user, thread, post, thread_update
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert not feed_data["items"][1]["hide_url"]


def test_thread_posts_feed_doesnt_mark_thread_update_as_unhideable_by_user(
    request_factory, user, thread, post, hidden_thread_update
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, thread, [post], [hidden_thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == hidden_thread_update
    assert not feed_data["items"][1]["unhide_url"]


def test_thread_posts_feed_doesnt_mark_thread_update_as_deletable_by_user(
    request_factory, user, thread, post, thread_update
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert not feed_data["items"][1]["delete_url"]


def test_thread_posts_feed_marks_thread_update_as_hidable_by_moderator(
    request_factory, moderator, thread, post, thread_update
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert feed_data["items"][1]["hide_url"]


def test_thread_posts_feed_marks_thread_update_as_unhideable_by_moderator(
    request_factory, moderator, thread, post, hidden_thread_update
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, thread, [post], [hidden_thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == hidden_thread_update
    assert feed_data["items"][1]["unhide_url"]


def test_thread_posts_feed_marks_thread_update_as_deletable_by_moderator(
    request_factory, moderator, thread, post, thread_update
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(request, thread, [post], [thread_update])
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == thread_update
    assert feed_data["items"][1]["delete_url"]


def test_private_thread_posts_feed_doesnt_mark_thread_update_as_hidable_by_user(
    request_factory,
    user,
    user_private_thread,
    private_thread_post,
    private_thread_update,
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(
        request, user_private_thread, [private_thread_post], [private_thread_update]
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == private_thread_update
    assert not feed_data["items"][1]["hide_url"]


def test_private_thread_posts_feed_doesnt_mark_thread_update_as_unhideable_by_user(
    request_factory,
    user,
    user_private_thread,
    private_thread_post,
    hidden_private_thread_update,
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(
        request,
        user_private_thread,
        [private_thread_post],
        [hidden_private_thread_update],
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == hidden_private_thread_update
    assert not feed_data["items"][1]["unhide_url"]


def test_private_thread_posts_feed_doesnt_mark_thread_update_as_deletable_by_user(
    request_factory,
    user,
    user_private_thread,
    private_thread_post,
    private_thread_update,
):
    request = request_factory(user)

    posts_feed = ThreadPostsFeed(
        request, user_private_thread, [private_thread_post], [private_thread_update]
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == private_thread_update
    assert not feed_data["items"][1]["delete_url"]


def test_private_thread_posts_feed_marks_thread_update_as_hidable_by_moderator(
    request_factory,
    moderator,
    user_private_thread,
    private_thread_post,
    private_thread_update,
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(
        request, user_private_thread, [private_thread_post], [private_thread_update]
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == private_thread_update
    assert feed_data["items"][1]["hide_url"]


def test_private_thread_posts_feed_marks_thread_update_as_unhideable_by_moderator(
    request_factory,
    moderator,
    user_private_thread,
    private_thread_post,
    hidden_private_thread_update,
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(
        request,
        user_private_thread,
        [private_thread_post],
        [hidden_private_thread_update],
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == hidden_private_thread_update
    assert feed_data["items"][1]["unhide_url"]


def test_private_thread_posts_feed_marks_thread_update_as_deletable_by_moderator(
    request_factory,
    moderator,
    user_private_thread,
    private_thread_post,
    private_thread_update,
):
    request = request_factory(moderator)

    posts_feed = ThreadPostsFeed(
        request, user_private_thread, [private_thread_post], [private_thread_update]
    )
    feed_data = posts_feed.get_context_data()

    assert feed_data["items"][1]["thread_update"] == private_thread_update
    assert feed_data["items"][1]["delete_url"]
