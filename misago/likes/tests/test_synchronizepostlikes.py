from io import StringIO

import pytest
from django.core import management

from ..management.commands import synchronizepostlikes
from ..models import Like


def call_command():
    command = synchronizepostlikes.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines() if l.strip())


def test_synchronizepostlikes_command_does_nothing_if_there_are_no_posts(db):
    command_output = call_command()

    assert command_output[-2:] == (
        "Synchronized 0 posts with likes.",
        "Removed outdated likes data from 0 posts.",
    )


def test_synchronizepostlikes_command_synchronizes_posts_likes(post, user_reply, user):
    Like.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post=user_reply,
        user=user,
        user_name=user.username,
        user_slug=user.slug,
    )

    Like.objects.create(
        category_id=post.category_id,
        thread_id=post.thread_id,
        post=post,
        user_name="DeletedUser",
        user_slug="deleteduser",
    )

    command_output = call_command()

    post.refresh_from_db()
    assert post.likes == 1
    assert post.last_likes == [{"id": None, "username": "DeletedUser"}]

    user_reply.refresh_from_db()
    assert user_reply.likes == 1
    assert user_reply.last_likes == [{"id": user.id, "username": user.username}]

    assert command_output[-2:] == (
        "Synchronized 2 posts with likes.",
        "Removed outdated likes data from 0 posts.",
    )


def test_synchronizepostlikes_command_clears_invalid_posts_likes_data(post):
    post.likes = 42
    post.last_likes = ["a", "b", "c"]
    post.save()

    command_output = call_command()

    post.refresh_from_db()
    assert post.likes == 0
    assert post.last_likes is None

    assert command_output[-2:] == (
        "Synchronized 0 posts with likes.",
        "Removed outdated likes data from one post.",
    )
