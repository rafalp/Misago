import pytest

from ..create import create_post_edit
from ..hide import hide_post_edit


@pytest.fixture
def post_edit(post):
    return create_post_edit(
        post=post,
        user="User",
        old_content="Old",
        new_content="New",
    )


@pytest.fixture
def hidden_post_edit(post, moderator):
    post_edit = create_post_edit(
        post=post,
        user="User",
        old_content="Lorem",
        new_content="Ipsum",
    )

    hide_post_edit(post_edit, moderator)

    return post_edit
