from ...parser.parse import parse
from ..state import StartState


def test_start_state_initializes_thread_and_post(user_request, default_category):
    state = StartState(user_request, default_category)

    assert state.thread
    assert state.thread.starter == user_request.user
    assert state.thread.starter_name == user_request.user.username
    assert state.thread.starter_slug == user_request.user.slug
    assert state.thread.last_poster == user_request.user
    assert state.thread.last_poster_name == user_request.user.username
    assert state.thread.last_poster_slug == user_request.user.slug
    assert state.thread.category == default_category
    assert state.thread.started_at == state.timestamp
    assert state.thread.last_posted_at == state.timestamp

    assert state.post
    assert state.post.poster == user_request.user
    assert state.post.poster_name == user_request.user.username
    assert state.post.category == default_category
    assert state.post.posted_at == state.timestamp


def test_start_state_stores_category_state(user_request, default_category):
    state = StartState(user_request, default_category)
    assert state.get_object_state(default_category)


def test_start_state_save_saves_thread_and_post(user_request, default_category):
    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.save()
    state.save_action(user_request, state)

    assert state.thread.id
    assert state.post.id
    assert state.post.thread == state.thread


def test_start_state_save_saves_post_search_document(user_request, default_category):
    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.save()
    state.save_action(user_request, state)

    assert state.post.search_document == "Test thread\n\nHello world"


def test_start_state_updates_category(user_request, default_category):
    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.save()
    state.save_action(user_request, state)

    default_category.refresh_from_db()
    assert default_category.threads == 1
    assert default_category.posts == 1
    assert default_category.last_thread == state.thread
    assert default_category.last_posted_at == state.thread.last_posted_at
    assert default_category.last_poster == state.thread.last_poster
    assert default_category.last_poster_name == state.thread.last_poster_name
    assert default_category.last_poster_slug == state.thread.last_poster_slug


def test_start_state_updates_user(user_request, default_category, user):
    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.save()
    state.save_action(user_request, state)

    user.refresh_from_db()
    assert user.threads == 1
    assert user.posts == 1
    assert user.last_posted_at == state.timestamp


def test_start_state_assigns_attachments_to_category_thread_and_post(
    user_request, default_category, user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post

    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_attachments([attachment])
    state.save()
    state.save_action(user_request, state)

    attachment.refresh_from_db()
    assert attachment.category == default_category
    assert attachment.thread == state.thread
    assert attachment.post == state.post
    assert attachment.uploaded_at == state.timestamp


def test_start_state_deletes_unused_attachments(
    user_request, default_category, user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post

    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_attachments([attachment])
    state.set_delete_attachments([attachment])
    state.save()
    state.save_action(user_request, state)

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted


def test_start_state_delete_attachments_excludes_unknown_attachments(
    user_request, default_category, user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    assert attachment.category == post.category
    assert attachment.thread == post.thread
    assert attachment.post == post

    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world"))
    state.set_delete_attachments([attachment])
    state.save()
    state.save_action(user_request, state)

    attachment.refresh_from_db()
    assert attachment.category == post.category
    assert attachment.thread == post.thread
    assert attachment.post == post
    assert not attachment.is_deleted


def test_start_state_schedules_post_upgrade_for_post_with_code_block(
    mock_upgrade_post_content, user_request, default_category
):
    state = StartState(user_request, default_category)
    state.set_thread_title("Test thread")
    state.set_post_message(parse("Hello world\n[code=python]add(1, 3)[/code]"))
    state.save()
    state.save_action(user_request, state)

    assert state.thread.id
    assert state.post.id
    assert state.post.thread == state.thread

    mock_upgrade_post_content.delay.assert_called_once_with(
        state.post.id, state.post.sha256_checksum
    )
