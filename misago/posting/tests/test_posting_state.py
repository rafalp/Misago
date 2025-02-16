from unittest.mock import patch

from ..state.base import PostingState


def test_posting_state_stores_request(user_request):
    state = PostingState(user_request)
    assert state.request == user_request


def test_posting_state_stores_request_user(user_request):
    state = PostingState(user_request)
    assert state.user == user_request.user


def test_posting_state_stores_current_timestamp(user_request):
    state = PostingState(user_request)
    assert state.timestamp


def test_posting_state_stores_original_user_state(user_request):
    state = PostingState(user_request)
    assert state.get_object_state(user_request.user)


def test_posting_state_stores_original_obj_state(user_request, default_category):
    state = PostingState(user_request)
    state.store_object_state(default_category)
    assert state.get_object_state(default_category)


def test_posting_state_returns_list_of_changed_obj_attributes(
    user_request, default_category
):
    state = PostingState(user_request)
    state.store_object_state(default_category)

    default_category.name = "Updated"
    default_category.threads = 2000

    assert state.get_object_changed_fields(default_category) == {"name", "threads"}


def test_posting_state_returns_list_of_changed_obj_foreign_keys(
    user_request, default_category
):
    state = PostingState(user_request)
    state.store_object_state(default_category)

    default_category.last_poster = user_request.user

    assert state.get_object_changed_fields(default_category) == {"last_poster"}


def test_posting_state_updates_only_changed_obj_attributes(
    user_request, default_category
):
    state = PostingState(user_request)
    state.store_object_state(default_category)

    default_category.name = "Updated"
    default_category.last_poster = user_request.user

    with patch.object(default_category, "save") as mock_save:
        state.update_object(default_category)
        mock_save.assert_called_once_with(update_fields={"name", "last_poster"})


def test_posting_state_set_thread_title_updates_thread_title_and_slug(
    user_request, thread
):
    state = PostingState(user_request)
    state.thread = thread
    state.set_thread_title("Test thread")

    assert state.thread.title == "Test thread"
    assert state.thread.slug == "test-thread"


def test_posting_state_set_post_message_updates_post_contents(user_request, post):
    state = PostingState(user_request)
    state.post = post
    state.set_post_message("Hello world")

    assert post.original == "Hello world"
    assert post.parsed == "<p>Hello world</p>"

    assert state.message_ast == [
        {
            "type": "paragraph",
            "children": [
                {"type": "text", "text": "Hello world"},
            ],
        },
    ]
    assert state.message_metadata == {
        "outbound-links": set(),
        "posts": {"ids": set(), "objs": {}},
        "attachments": set(),
        "usernames": set(),
        "users": {},
    }


def test_posting_state_set_post_message_stores_attachments_ids_in_post_metadata(
    user_request, post
):
    state = PostingState(user_request)
    state.post = post
    state.set_post_message("<attachment=image.png:123>")

    assert post.original == "<attachment=image.png:123>"
    assert post.parsed == (
        '<div class="rich-text-attachment-group">'
        "<attachment=image.png:image-png:123>"
        "</div>"
    )
    assert post.metadata == {"attachments": [123]}

    assert state.message_ast == [
        {
            "type": "attachment-group",
            "children": [
                {
                    "type": "attachment",
                    "name": "image.png",
                    "slug": "image-png",
                    "id": 123,
                },
            ],
        },
    ]
    assert state.message_metadata == {
        "outbound-links": set(),
        "posts": {"ids": set(), "objs": {}},
        "attachments": {123},
        "usernames": set(),
        "users": {},
    }
