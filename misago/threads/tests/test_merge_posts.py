import pytest

from ...likes.like import like_post
from ...notifications.users import notify_user
from ...postedits.create import create_post_edit
from ...solutions.select import select_thread_solution
from ..merge import (
    get_post_merge_conflicts,
    get_post_merge_form_fields,
    merge_posts,
)
from ..models import Post


@pytest.fixture
def posts(thread_reply_factory, thread):
    target = thread_reply_factory(
        thread,
        original="Lorem ipsum",
        parsed="<p>Lorem ipsum</p>",
        search_document="Lorem",
    )
    other_post = thread_reply_factory(
        thread,
        original="Dolor met",
        parsed="<p>Dolor met</p>",
        search_document="Dolor",
    )

    return (target, other_post)


@pytest.fixture
def target(posts):
    return posts[0]


@pytest.fixture
def other_post(posts):
    return posts[1]


def test_get_post_merge_conflicts_returns_dict(post, reply):
    conflicts = get_post_merge_conflicts([post, reply])
    assert isinstance(conflicts, dict)


def test_get_post_merge_form_fields_returns_dict():
    fields = get_post_merge_form_fields({})
    assert isinstance(fields, dict)


def test_get_merge_posts_merges_posts_contents(user, target, other_post):
    merge_posts(target, [other_post], {}, user)

    assert target.original == "Lorem ipsum\n\nDolor met"
    assert target.parsed == "<p>Lorem ipsum</p>\n<p>Dolor met</p>"
    assert target.search_document == "Lorem\n\nDolor"


def test_get_merge_posts_merges_posts_metadata(user, target, other_post):
    target.metadata = {
        "attachments": [1, 2, 3],
        "highlight_code": ["asm", "python"],
    }
    other_post.metadata = {"highlight_code": ["python", "php"], "posts": [6, 5, 4]}

    merge_posts(target, [other_post], {}, user)

    assert target.metadata == {
        "attachments": [1, 2, 3],
        "highlight_code": ["asm", "php", "python"],
        "posts": [6, 5, 4],
    }


def test_merge_posts_updates_thread_last_post(user, thread, target, other_post):
    merge_posts(target, [other_post], {}, user)

    thread.refresh_from_db()
    assert thread.last_post == target


def test_merge_posts_merges_solution(user, thread, target, other_post):
    select_thread_solution(thread, other_post, "John")

    merge_posts(target, [other_post], {}, user)

    thread.refresh_from_db()
    assert thread.solution == target


def test_merge_posts_merges_attachments(user, target, other_post, text_attachment):
    text_attachment.associate_with_post(other_post)
    text_attachment.save()

    merge_posts(target, [other_post], {}, user)

    text_attachment.refresh_from_db()
    assert text_attachment.post == target


def test_merge_posts_merges_likes(user, target, other_post):
    target_like = like_post(target, "Bob")
    other_post_like = like_post(other_post, "Alice")

    merge_posts(target, [other_post], {}, user)

    target.refresh_from_db()
    assert target.likes == 2
    assert target.last_likes == [
        {"id": None, "username": "Alice"},
        {"id": None, "username": "Bob"},
    ]

    target_like.refresh_from_db()
    assert target_like.post == target

    other_post_like.refresh_from_db()
    assert other_post_like.post == target


def test_merge_posts_merges_post_edits(user, target, other_post):
    target_edit = create_post_edit(
        post=target,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )
    other_post_edit = create_post_edit(
        post=other_post,
        user="DeletedUser",
        old_content="Lorem",
        new_content="Ipsum",
    )

    merge_posts(target, [other_post], {}, user)

    target_edit.refresh_from_db()
    assert target_edit.post == target

    other_post_edit.refresh_from_db()
    assert other_post_edit.post == target


def test_merge_posts_merges_post_edits_count(user, target, other_post):
    target.edits = 1
    target.save()

    other_post.edits = 2
    other_post.save()

    merge_posts(target, [other_post], {}, user)

    target.refresh_from_db()
    assert target.edits == 4  # merge also counts as a new edit


def test_merge_posts_merges_thread_post_notifications(user, target, other_post):
    target_notification = notify_user(
        user,
        "TEST",
        "DeletedUser",
        target.category,
        target.thread,
        target,
    )
    other_post_notification = notify_user(
        user,
        "TEST",
        "DeletedUser",
        other_post.category,
        other_post.thread,
        other_post,
    )

    merge_posts(target, [other_post], {}, user)

    target_notification.refresh_from_db()
    assert target_notification.post == target

    other_post_notification.refresh_from_db()
    assert other_post_notification.post == target


def test_get_merge_posts_deletes_old_posts(user, target, other_post):
    merge_posts(target, [other_post], {}, user)

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()


def test_get_merge_posts_updates_target_last_edit_data(user, target, other_post):
    merge_posts(target, [other_post], {}, user, "Hello world")

    assert target.updated_at
    assert target.edits == 1
    assert target.last_edit_reason == "Hello world"
    assert target.last_editor == user
    assert target.last_editor_name == user.username
    assert target.last_editor_slug == user.slug


def test_get_merge_posts_updates_target_last_edit_data_for_deleted_user(
    target, other_post
):
    merge_posts(target, [other_post], {}, "AutoMod", "Hello world")

    assert target.updated_at
    assert target.edits == 1
    assert target.last_edit_reason == "Hello world"
    assert target.last_editor is None
    assert target.last_editor_name == "AutoMod"
    assert target.last_editor_slug == "automod"


def test_merge_posts_doesnt_save_target_if_commit_is_false(user, target, other_post):
    assert merge_posts(target, [other_post], {}, user, "Hello world", commit=False)
    assert target.updated_at
    assert target.edits == 1
    assert target.last_edit_reason == "Hello world"
    assert target.last_editor == user
    assert target.last_editor_name == user.username
    assert target.last_editor_slug == user.slug

    target.refresh_from_db()
    assert not target.updated_at
    assert not target.edits
    assert not target.last_edit_reason
    assert not target.last_editor
    assert not target.last_editor_name
    assert not target.last_editor_slug
