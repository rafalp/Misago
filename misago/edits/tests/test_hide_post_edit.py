from ..hide import hide_post_edit


def test_hide_post_edit_hides_edit(post_edit, user):
    assert not post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name is None
    assert post_edit.hidden_by_slug is None
    assert post_edit.hidden_at is None

    hide_post_edit(post_edit, user)

    assert post_edit.is_hidden
    assert post_edit.hidden_by == user
    assert post_edit.hidden_by_name == user.username
    assert post_edit.hidden_by_slug == user.slug
    assert post_edit.hidden_at

    post_edit.refresh_from_db()

    assert post_edit.is_hidden
    assert post_edit.hidden_by == user
    assert post_edit.hidden_by_name == user.username
    assert post_edit.hidden_by_slug == user.slug
    assert post_edit.hidden_at


def test_hide_post_edit_hides_edit_by_deleted_user(post_edit):
    assert not post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name is None
    assert post_edit.hidden_by_slug is None
    assert post_edit.hidden_at is None

    hide_post_edit(post_edit, "DeletedUser")

    assert post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name == "DeletedUser"
    assert post_edit.hidden_by_slug == "deleteduser"
    assert post_edit.hidden_at

    post_edit.refresh_from_db()

    assert post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name == "DeletedUser"
    assert post_edit.hidden_by_slug == "deleteduser"
    assert post_edit.hidden_at


def test_hide_post_edit_without_commit_doesnt_save_post_edit(
    django_assert_num_queries, post_edit, user
):
    assert not post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name is None
    assert post_edit.hidden_by_slug is None
    assert post_edit.hidden_at is None

    with django_assert_num_queries(0):
        hide_post_edit(post_edit, user, commit=False)

    assert post_edit.is_hidden
    assert post_edit.hidden_by == user
    assert post_edit.hidden_by_name == user.username
    assert post_edit.hidden_by_slug == user.slug
    assert post_edit.hidden_at

    post_edit.refresh_from_db()

    assert not post_edit.is_hidden
    assert post_edit.hidden_by is None
    assert post_edit.hidden_by_name is None
    assert post_edit.hidden_by_slug is None
    assert post_edit.hidden_at is None
