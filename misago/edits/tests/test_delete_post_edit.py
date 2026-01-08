import pytest

from ..delete import delete_post_edit
from ..models import PostEdit


def test_delete_post_edit_deletes_post_edit(post_edit):
    delete_post_edit(post_edit)

    with pytest.raises(PostEdit.DoesNotExist):
        post_edit.refresh_from_db()


def test_delete_post_edit_doesnt_delete_post_edit_if_commit_is_false(
    django_assert_num_queries, post_edit
):
    with django_assert_num_queries(0):
        delete_post_edit(post_edit, commit=False)

    post_edit.refresh_from_db()
