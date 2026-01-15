from ..create import create_post_edit
from ..restore import restore_post_edit


def test_restore_post_edit_restores_post(post, user):
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    _, new_post_edit = restore_post_edit(post_edit, user)

    assert new_post_edit.id

    assert post.original == "Lorem ipsum"
    assert post.parsed == "<p>Lorem ipsum</p>"
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason is None

    post.refresh_from_db()

    assert post.original == "Lorem ipsum"
    assert post.parsed == "<p>Lorem ipsum</p>"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug
    assert post.last_edit_reason is None


def test_restore_post_edit_restores_post_by_deleted_user(post, user):
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    _, new_post_edit = restore_post_edit(post_edit, "DeletedUser")

    assert new_post_edit.id

    assert post.original == "Lorem ipsum"
    assert post.parsed == "<p>Lorem ipsum</p>"
    assert post.last_editor is None
    assert post.last_editor_name == "DeletedUser"
    assert post.last_editor_slug == "deleteduser"
    assert post.last_edit_reason is None

    post.refresh_from_db()

    assert post.original == "Lorem ipsum"
    assert post.parsed == "<p>Lorem ipsum</p>"
    assert post.updated_at
    assert post.edits == 1
    assert post.last_editor is None
    assert post.last_editor_name == "DeletedUser"
    assert post.last_editor_slug == "deleteduser"
    assert post.last_edit_reason is None


def test_restore_post_edit_without_commit_doesnt_save_post_and_post_edit(
    django_assert_num_queries, post, user
):
    post_edit = create_post_edit(
        post=post,
        user=user,
        old_content="Lorem ipsum",
        new_content=post.original,
    )

    # New post edit creation runs query to snapshot existing attachments
    with django_assert_num_queries(1):
        _, new_post_edit = restore_post_edit(post_edit, "DeletedUser", commit=False)

    assert not new_post_edit.id

    assert post.original == "Lorem ipsum"
    assert post.parsed == "<p>Lorem ipsum</p>"
    assert post.last_editor is None
    assert post.last_editor_name == "DeletedUser"
    assert post.last_editor_slug == "deleteduser"
    assert post.last_edit_reason is None

    post.refresh_from_db()

    assert post.original != "Lorem ipsum"
    assert post.parsed != "<p>Lorem ipsum</p>"
    assert post.updated_at is None
    assert post.edits == 0
    assert post.last_editor is None
    assert post.last_editor_name is None
    assert post.last_editor_slug is None
    assert post.last_edit_reason is None
