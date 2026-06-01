import pytest

from ...postedits.create import create_post_edit
from ...postedits.models import PostEdit
from ...likes.like import like_post
from ...likes.models import Like
from ...notifications.models import Notification
from ...notifications.users import notify_user
from ..delete import delete_post
from ..models import Post


def test_delete_post_deletes_threads_only_post(thread, post):
    delete_post(post)

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    thread.refresh_from_db()
    assert thread.first_post is None
    assert thread.last_post is None


def test_delete_post_deletes_threads_first_post(thread, post, reply):
    delete_post(post)

    with pytest.raises(Post.DoesNotExist):
        post.refresh_from_db()

    thread.refresh_from_db()
    assert thread.first_post is None
    assert thread.last_post == reply


def test_delete_post_deletes_threads_last_post(thread, post, reply):
    delete_post(reply)

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    thread.refresh_from_db()
    assert thread.first_post == post
    assert thread.last_post is None


def test_delete_post_deletes_thread_post_like(thread, reply):
    post_like = like_post(reply, "DeletedUser")

    delete_post(reply)

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Like.DoesNotExist):
        post_like.refresh_from_db()


def test_delete_post_deletes_thread_post_edit(thread, reply):
    post_edit = create_post_edit(
        post=reply,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )

    delete_post(reply)

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_delete_post_deletes_thread_post_notification(user, thread, reply):
    notification = notify_user(
        user, "TEST", "DeletedUser", thread.category, thread, reply
    )

    delete_post(reply)

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    with pytest.raises(Notification.DoesNotExist):
        notification.refresh_from_db()


def test_delete_post_marks_attachments_for_deletion(thread, reply, text_attachment):
    text_attachment.associate_with_post(reply)
    text_attachment.save()

    delete_post(reply)

    with pytest.raises(Post.DoesNotExist):
        reply.refresh_from_db()

    text_attachment.refresh_from_db()
    assert text_attachment.category is None
    assert text_attachment.thread is None
    assert text_attachment.post is None
    assert text_attachment.is_deleted
