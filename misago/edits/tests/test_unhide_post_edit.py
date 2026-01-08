from ..hide import unhide_post_edit


def test_unhide_post_edit_unhides_edit(hidden_post_edit):
    assert hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by
    assert hidden_post_edit.hidden_by_name
    assert hidden_post_edit.hidden_by_slug
    assert hidden_post_edit.hidden_at

    unhide_post_edit(hidden_post_edit)

    assert not hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by is None
    assert hidden_post_edit.hidden_by_name is None
    assert hidden_post_edit.hidden_by_slug is None
    assert hidden_post_edit.hidden_at is None

    hidden_post_edit.refresh_from_db()

    assert not hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by is None
    assert hidden_post_edit.hidden_by_name is None
    assert hidden_post_edit.hidden_by_slug is None
    assert hidden_post_edit.hidden_at is None


def test_unhide_post_edit_without_commit_doesnt_save_post_edit(
    django_assert_num_queries, hidden_post_edit
):
    assert hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by
    assert hidden_post_edit.hidden_by_name
    assert hidden_post_edit.hidden_by_slug
    assert hidden_post_edit.hidden_at

    with django_assert_num_queries(0):
        unhide_post_edit(hidden_post_edit, commit=False)

    assert not hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by is None
    assert hidden_post_edit.hidden_by_name is None
    assert hidden_post_edit.hidden_by_slug is None
    assert hidden_post_edit.hidden_at is None

    hidden_post_edit.refresh_from_db()

    assert hidden_post_edit.is_hidden
    assert hidden_post_edit.hidden_by
    assert hidden_post_edit.hidden_by_name
    assert hidden_post_edit.hidden_by_slug
    assert hidden_post_edit.hidden_at
