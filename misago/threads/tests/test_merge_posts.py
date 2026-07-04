import pytest

from ..merge import (
    get_post_merge_conflicts,
    get_post_merge_form_fields,
    merge_posts,
)
from ..models import Post


def test_get_post_merge_conflicts_returns_dict(post, reply):
    conflicts = get_post_merge_conflicts([post, reply])
    assert isinstance(conflicts, dict)


def test_get_post_merge_form_fields_returns_dict():
    fields = get_post_merge_form_fields({})
    assert isinstance(fields, dict)


def test_get_merge_posts_merges_posts_contents(thread_reply_factory, thread):
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

    merge_posts(target, [other_post], {})

    assert target.original == "Lorem ipsum\n\nDolor met"
    assert target.parsed == "<p>Lorem ipsum</p>\n<p>Dolor met</p>"
    assert target.search_document == "Lorem\n\nDolor"


def test_get_merge_posts_merges_posts_metadata(thread_reply_factory, thread):
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

    target.metadata = {
        "attachments": [1, 2, 3],
        "highlight_code": ["asm", "python"],
    }
    other_post.metadata = {"highlight_code": ["python", "php"], "posts": [6, 5, 4]}

    merge_posts(target, [other_post], {})

    assert target.metadata == {
        "attachments": [1, 2, 3],
        "highlight_code": ["asm", "php", "python"],
        "posts": [6, 5, 4],
    }


def test_get_merge_posts_deletes_old_posts(thread_reply_factory, thread):
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

    merge_posts(target, [other_post], {})

    with pytest.raises(Post.DoesNotExist):
        other_post.refresh_from_db()
