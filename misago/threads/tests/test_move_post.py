import pytest

from ...likes.like import like_post
from ...notifications.users import notify_user
from ...postedits.create import create_post_edit
from ..move import move_post


@pytest.fixture
def new_thread(sibling_category, other_thread):
    other_thread.category = sibling_category
    other_thread.save()

    return other_thread


def test_move_post_moves_post(new_thread, reply):
    move_post(reply, new_thread)

    assert reply.category == new_thread.category
    assert reply.thread == new_thread

    reply.refresh_from_db()
    assert reply.category == new_thread.category
    assert reply.thread == new_thread


def test_move_post_moves_post_attachment(new_thread, reply, text_attachment):
    text_attachment.associate_with_post(reply)
    text_attachment.save()

    move_post(reply, new_thread)

    text_attachment.refresh_from_db()
    assert text_attachment.category == new_thread.category
    assert text_attachment.thread == new_thread


def test_move_post_moves_post_like(new_thread, reply):
    post_like = like_post(reply, "DeletedUser")

    move_post(reply, new_thread)

    post_like.refresh_from_db()
    assert post_like.category == new_thread.category
    assert post_like.thread == new_thread


def test_move_post_moves_post_notification(user, new_thread, thread, reply):
    notification = notify_user(
        user, "TEST", "DeletedUser", thread.category, thread, reply
    )

    move_post(reply, new_thread)

    notification.refresh_from_db()
    assert notification.category == new_thread.category
    assert notification.thread == new_thread


def test_move_post_moves_post_edit(new_thread, reply):
    post_edit = create_post_edit(
        post=reply,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )

    move_post(reply, new_thread)

    post_edit.refresh_from_db()
    assert post_edit.category == new_thread.category
    assert post_edit.thread == new_thread


def test_move_post_doesnt_save_post_if_commit_is_false(new_thread, thread, reply):
    move_post(reply, new_thread, commit=False)

    assert reply.category == new_thread.category
    assert reply.thread == new_thread

    reply.refresh_from_db()
    assert reply.category == thread.category
    assert reply.thread == thread
