import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ...attachments.enums import AllowedAttachments
from ...attachments.models import Attachment
from ...conf.test import override_dynamic_settings
from ...edits.models import PostEdit
from ...permissions.enums import CanUploadAttachments
from ...privatethreads.models import PrivateThreadMember
from ...readtracker.models import ReadCategory
from ...readtracker.tracker import mark_thread_read
from ...test import assert_contains, assert_contains_element, assert_not_contains
from ..forms import PostForm
from ..formsets import Formset


def test_private_thread_reply_view_displays_login_required_page_to_anonymous_user(
    client, other_user_private_thread
):
    response = client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Sign in to reply to threads", status_code=401)


def test_private_thread_reply_view_shows_error_403_to_users_without_private_threads_permission(
    user_client, members_group, other_user_private_thread
):
    members_group.can_use_private_threads = False
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "You can&#x27;t use private threads.", 403)


def test_private_thread_reply_view_shows_error_404_if_thread_doesnt_exist(user_client):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": 100,
                "slug": "not-found",
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_reply_view_shows_error_404_to_users_who_cant_see_thread(
    user_client, private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert response.status_code == 404


def test_private_thread_reply_view_shows_error_403_to_user_if_thread_has_no_other_members(
    user_client, user, private_thread
):
    PrivateThreadMember.objects.create(user=user, thread=private_thread)

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": private_thread.id,
                "slug": private_thread.slug,
            },
        )
    )
    assert_contains(
        response, "You can&#x27;t reply to a private thread without other members.", 403
    )


def test_private_thread_reply_view_displays_posting_form(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)


def test_private_thread_reply_view_displays_posting_form_with_quoted_post(
    thread_reply_factory, user_client, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread, poster="QuotedUser", original="Bread and butter"
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote={post.id}"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, f"[quote=QuotedUser, post: {post.id}]")
    assert_contains(response, post.original)
    assert_contains(response, "[/quote]")


def test_private_thread_reply_view_doesnt_init_posting_form_with_hidden_quoted_post(
    thread_reply_factory, user_client, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster="QuotedUser",
        original="Bread and butter",
        is_hidden=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote={post.id}"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=QuotedUser, post: {post.id}]")
    assert_not_contains(response, post.original)
    assert_not_contains(response, "[/quote]")


@pytest.mark.xfail(reason="unapproved posts visible in private threads")
def test_private_thread_reply_view_doesnt_init_posting_form_with_invisible_quoted_post(
    thread_reply_factory, user_client, other_user_private_thread
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster="QuotedUser",
        original="Bread and butter",
        is_unapproved=True,
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote={post.id}"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=QuotedUser, post: {post.id}]")
    assert_not_contains(response, post.original)
    assert_not_contains(response, "[/quote]")


def test_private_thread_reply_view_doesnt_init_posting_form_with_other_thread_quoted_post(
    thread_reply_factory, user_client, other_user_private_thread, user_private_thread
):
    post = thread_reply_factory(
        user_private_thread, poster="QuotedUser", original="Bread and butter"
    )

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote={post.id}"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=QuotedUser, post: {post.id}]")
    assert_not_contains(response, post.original)
    assert_not_contains(response, "[/quote]")


def test_private_thread_reply_view_doesnt_init_posting_form_with_non_existing_quoted_post(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote={other_user_private_thread.last_post_id * 1000}"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=User, post:")


def test_private_thread_reply_view_doesnt_init_posting_form_with_invalid_quoted_post(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote=invalid"
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=")


def test_private_thread_reply_view_doesnt_init_posting_form_with_empty_quoted_post(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"?quote="
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, f"[quote=")


def test_private_thread_reply_view_posts_new_reply(
    user_client, other_user_private_thread, mock_notify_on_new_thread_reply
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_posts_new_reply_in_htmx(
    user_client, other_user_private_thread, mock_notify_on_new_thread_reply
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 204

    reply = other_user_private_thread.post_set.last()

    assert (
        response["hx-redirect"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_posts_new_reply_in_quick_reply(
    user_client, other_user_private_thread, mock_notify_on_new_thread_reply
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_posts_new_reply_in_quick_reply_with_htmx(
    user_client, other_user_private_thread, mock_notify_on_new_thread_reply
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = other_user_private_thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_posted_reply_in_quick_reply_with_htmx_is_read(
    user_client, user, other_user_private_thread, mock_notify_on_new_thread_reply
):
    mark_thread_read(
        user, other_user_private_thread, other_user_private_thread.last_post.posted_at
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply = other_user_private_thread.post_set.last()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, f"<p>This is a reply!</p>")

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)

    ReadCategory.objects.get(
        user=user,
        category=other_user_private_thread.category,
        read_time=reply.posted_at,
    )


def test_private_thread_reply_view_previews_message(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_quick_reply(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_previews_message_in_quick_reply_with_htmx(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "This is a reply!",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert_contains(response, "Post reply")
    assert_contains(response, "Message preview")


def test_private_thread_reply_view_validates_post(
    user_client, other_user_private_thread
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "?",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response, "Posted message must be at least 5 characters long (it has 1)."
    )


def test_private_thread_reply_view_validates_posted_contents(
    user_client, other_user_private_thread, posted_contents_validator
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a spam message",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "Your message contains spam!")


@override_dynamic_settings(merge_concurrent_posts=0)
def test_private_thread_reply_view_runs_flood_control(
    thread_reply_factory, user_client, user, other_user_private_thread
):
    thread_reply_factory(other_user_private_thread, poster=user)

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "This is a flood message",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(
        response, "You can&#x27;t post a new message so soon after the previous one."
    )


def test_private_thread_reply_view_merges_reply_with_users_recent_post(
    thread_reply_factory, user, user_client, other_user_private_thread
):
    reply = thread_reply_factory(
        other_user_private_thread, poster=user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.original == "Previous message\n\nReply contents"

    post_edit = PostEdit.objects.get(post=reply)
    assert not post_edit.edit_reason
    assert post_edit.added_content == 2
    assert post_edit.removed_content == 0


def test_private_thread_reply_view_merges_reply_with_users_recent_post_in_htmx(
    thread_reply_factory, user, user_client, other_user_private_thread
):
    reply = thread_reply_factory(
        other_user_private_thread, poster=user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
            "quick_reply": "true",
        },
        headers={"hx-request": "true"},
    )
    assert response.status_code == 200

    reply.refresh_from_db()

    assert_contains(response, f"post-{reply.id}")
    assert_contains(response, reply.parsed)

    assert reply.original == "Previous message\n\nReply contents"


@override_dynamic_settings(merge_concurrent_posts=0, flood_control=0)
def test_private_thread_reply_view_doesnt_merge_reply_with_users_recent_post_if_feature_is_disabled(
    thread_reply_factory,
    user,
    user_client,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
):
    reply = thread_reply_factory(
        other_user_private_thread, poster=user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    other_user_private_thread.refresh_from_db()
    assert other_user_private_thread.last_post_id == reply.id + 1

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{other_user_private_thread.last_post_id}"
    )

    reply.refresh_from_db()
    assert reply.original == "Previous message"

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(
        other_user_private_thread.last_post_id
    )


@override_dynamic_settings(flood_control=0)
def test_private_thread_reply_view_doesnt_merge_reply_with_users_recent_post_in_preview(
    thread_reply_factory, user, user_client, other_user_private_thread
):
    thread_reply_factory(
        other_user_private_thread, poster=user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            "posting-post-post": "Reply contents",
        },
    )

    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "<p>Reply contents</p>")
    assert_not_contains(response, "<p>Previous message</p>")


@override_dynamic_settings(merge_concurrent_posts=1)
def test_private_thread_reply_view_doesnt_merge_reply_with_users_recent_post_if_its_too_old(
    thread_reply_factory,
    user,
    user_client,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster=user,
        original="Previous message",
        posted_at=-120,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.id == post.id + 1
    assert reply.original == "Reply contents"

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_doesnt_merge_reply_with_recent_post_if_its_by_other_user(
    thread_reply_factory,
    other_user,
    user_client,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
):
    post = thread_reply_factory(
        other_user_private_thread, poster=other_user, original="Previous message"
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.id == post.id + 1
    assert reply.original == "Reply contents"

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


@override_dynamic_settings(flood_control=0)
def test_private_thread_reply_view_doesnt_merge_reply_with_users_recent_post_if_its_hidden(
    thread_reply_factory,
    user,
    user_client,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster=user,
        original="Previous message",
        is_hidden=True,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.id == post.id + 1
    assert reply.original == "Reply contents"

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


@override_dynamic_settings(flood_control=0)
def test_private_thread_reply_view_doesnt_merge_reply_with_users_recent_post_if_its_not_editable(
    thread_reply_factory,
    user,
    user_client,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
):
    post = thread_reply_factory(
        other_user_private_thread,
        poster=user,
        original="Previous message",
        is_protected=True,
    )

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    reply = other_user_private_thread.post_set.last()

    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{reply.id}"
    )

    assert reply.id == post.id + 1
    assert reply.original == "Reply contents"

    mock_notify_on_new_thread_reply.delay.assert_called_once_with(reply.id)


def test_private_thread_reply_view_displays_attachments_form(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")


@override_dynamic_settings(allowed_attachment_types=AllowedAttachments.NONE.value)
def test_private_thread_reply_view_hides_attachments_form_if_uploads_are_disabled(
    user_client, other_user_private_thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, "misago-editor-attachments=")


@pytest.mark.parametrize(
    "permission", [CanUploadAttachments.THREADS, CanUploadAttachments.NEVER]
)
def test_private_thread_reply_view_hides_attachments_form_if_user_has_no_group_permission(
    members_group, user_client, other_user_private_thread, permission
):
    members_group.can_upload_attachments = permission
    members_group.save()

    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_not_contains(response, "misago-editor-attachments=")


def test_private_thread_reply_view_uploads_attachment_on_submit(
    user_client,
    user,
    other_user_private_thread,
    mock_notify_on_new_thread_reply,
    teardown_attachments,
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            "posting-post-post": "Reply contents",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert response.status_code == 302

    other_user_private_thread.refresh_from_db()

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id == other_user_private_thread.category_id
    assert attachment.thread_id == other_user_private_thread.id
    assert attachment.post_id == other_user_private_thread.last_post_id
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"

    mock_notify_on_new_thread_reply.delay.assert_called_once()


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_uploads_attachment_on_preview_or_upload(
    action_name, user_client, user, other_user_private_thread, teardown_attachments
):
    assert not Attachment.objects.exists()

    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            "posting-post-post": "Reply contents",
            "posting-post-upload": [
                SimpleUploadedFile("test.txt", b"Hello world!", "text/plain"),
            ],
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    other_user_private_thread.refresh_from_db()

    attachment = Attachment.objects.get(uploader=user)
    assert attachment.category_id is None
    assert attachment.thread_id is None
    assert attachment.post_id is None
    assert attachment.uploader_id == user.id
    assert not attachment.is_deleted
    assert attachment.name == "test.txt"

    assert_contains(response, attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_displays_image_attachment(
    action_name, user_client, other_user_private_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_image_attachment.name)
    assert_contains(response, user_image_attachment.get_absolute_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_image_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_displays_image_with_thumbnail_attachment(
    action_name, user_client, other_user_private_thread, user_image_thumbnail_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_image_thumbnail_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_image_thumbnail_attachment.name)
    assert_contains(response, user_image_thumbnail_attachment.get_thumbnail_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_image_thumbnail_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_displays_video_attachment(
    action_name, user_client, other_user_private_thread, user_video_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_video_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_video_attachment.name)
    assert_contains(response, user_video_attachment.get_absolute_url())
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_video_attachment.id,
    )


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_displays_file_attachment(
    action_name, user_client, other_user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains(response, user_text_attachment.name)
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )


def test_private_thread_reply_view_associates_unused_attachment_on_submit(
    user_client,
    other_user_private_thread,
    user_text_attachment,
    mock_notify_on_new_thread_reply,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert response.status_code == 302

    other_user_private_thread.refresh_from_db()

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id == other_user_private_thread.category_id
    assert user_text_attachment.thread_id == other_user_private_thread.id
    assert user_text_attachment.post_id == other_user_private_thread.last_post_id
    assert not user_text_attachment.is_deleted

    mock_notify_on_new_thread_reply.delay.assert_called_once()


def test_private_thread_reply_view_adds_attachment_to_deleted_list(
    user_client, other_user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.delete_attachment_field: str(user_text_attachment.id),
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_not_contains(response, user_text_attachment.name)
    assert_not_contains(response, user_text_attachment.get_absolute_url())


@pytest.mark.parametrize(
    "action_name", (Formset.preview_action, PostForm.upload_action)
)
def test_private_thread_reply_view_maintains_deleted_attachments_list(
    action_name, user_client, other_user_private_thread, user_text_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            action_name: "true",
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "Reply contents",
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "misago-editor-attachments=")

    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_contains_element(
        response,
        "input",
        type="hidden",
        name=PostForm.deleted_attachment_ids_field,
        value=user_text_attachment.id,
    )
    assert_not_contains(response, user_text_attachment.name)
    assert_not_contains(response, user_text_attachment.get_absolute_url())


def test_private_thread_reply_view_deletes_attachment_on_submit(
    user_client,
    other_user_private_thread,
    user_text_attachment,
    mock_notify_on_new_thread_reply,
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            PostForm.attachment_ids_field: [str(user_text_attachment.id)],
            PostForm.deleted_attachment_ids_field: [str(user_text_attachment.id)],
            "posting-post-post": "How's going?",
        },
    )
    assert response.status_code == 302

    other_user_private_thread.refresh_from_db()
    assert (
        response["location"]
        == reverse(
            "misago:private-thread",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        )
        + f"#post-{other_user_private_thread.last_post_id}"
    )

    user_text_attachment.refresh_from_db()
    assert user_text_attachment.category_id is None
    assert user_text_attachment.thread_id is None
    assert user_text_attachment.post_id is None
    assert user_text_attachment.is_deleted

    mock_notify_on_new_thread_reply.delay.assert_called_once()


def test_private_thread_reply_view_embeds_attachments_in_preview(
    user_client, other_user_private_thread, user_image_attachment
):
    response = user_client.post(
        reverse(
            "misago:private-thread-reply",
            kwargs={
                "thread_id": other_user_private_thread.id,
                "slug": other_user_private_thread.slug,
            },
        ),
        {
            Formset.preview_action: "true",
            PostForm.attachment_ids_field: [str(user_image_attachment.id)],
            "posting-post-post": (
                f"Attachment: <attachment={user_image_attachment.name}:{user_image_attachment.id}>"
            ),
        },
    )
    assert_contains(response, "Reply to thread")
    assert_contains(response, other_user_private_thread.title)
    assert_contains(response, "Message preview")
    assert_contains_element(response, "a", href=user_image_attachment.get_details_url())
    assert_contains_element(
        response, "img", src=user_image_attachment.get_absolute_url()
    )


def test_private_thread_reply_view_shows_error_if_thread_is_accessed(
    user_client, thread
):
    response = user_client.get(
        reverse(
            "misago:private-thread-reply",
            kwargs={"thread_id": thread.id, "slug": thread.slug},
        ),
    )
    assert_not_contains(response, "Reply to thread", status_code=404)
    assert_not_contains(response, thread.title, status_code=404)
