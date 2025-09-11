from ...parser.parse import parse
from ...threadupdates.create import create_split_thread_update
from ...threadupdates.enums import ThreadUpdateActionName
from ...threadupdates.models import ThreadUpdate
from ..state import PostEditState


def test_post_edit_state_save_updates_thread_title(user_request, other_user_thread):
    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_thread_title("Updated title")
    state.save()

    other_user_thread.refresh_from_db()

    assert other_user_thread.title == "Updated title"
    assert other_user_thread.slug == "updated-title"


def test_post_edit_state_save_updates_post(user, user_request, other_user_thread):
    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_post_message(parse("Edit reply"))
    state.save()

    post = other_user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edit reply"
    assert post.search_document == f"{other_user_thread.title}\n\nEdit reply"
    assert post.updated_at == state.timestamp
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug


def test_post_edit_state_save_updates_post_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    attachment = attachment_factory(text_file, uploader=user)
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post

    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_post_message(parse("Edit reply"))
    state.set_attachments([attachment])
    state.save()

    post_attachment.refresh_from_db()
    assert post_attachment.category == other_user_thread.category
    assert post_attachment.thread == other_user_thread
    assert post_attachment.post == post
    assert post_attachment.uploader == other_user
    assert post_attachment.uploaded_at < state.timestamp

    attachment.refresh_from_db()
    assert attachment.category == other_user_thread.category
    assert attachment.thread == other_user_thread
    assert attachment.post == post
    assert attachment.uploader == user
    assert attachment.uploaded_at == state.timestamp


def test_post_edit_state_save_deletes_post_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    attachment = attachment_factory(text_file, uploader=user, post=post)

    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_post_message(parse("Edit reply"))
    state.set_attachments([attachment, post_attachment])
    state.set_delete_attachments([attachment])
    state.save()

    post_attachment.refresh_from_db()
    assert post_attachment.category == other_user_thread.category
    assert post_attachment.thread == other_user_thread
    assert post_attachment.post == post
    assert post_attachment.uploader == other_user
    assert post_attachment.uploaded_at < state.timestamp

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert not attachment.uploader
    assert attachment.is_deleted


def test_post_edit_state_save_deletes_unused_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    unused_attachment = attachment_factory(text_file, uploader=user)

    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_post_message(parse("Edit reply"))
    state.set_attachments([unused_attachment, post_attachment])
    state.set_delete_attachments([unused_attachment])
    state.save()

    post_attachment.refresh_from_db()
    assert post_attachment.category == other_user_thread.category
    assert post_attachment.thread == other_user_thread
    assert post_attachment.post == post
    assert post_attachment.uploader == other_user
    assert post_attachment.uploaded_at < state.timestamp

    unused_attachment.refresh_from_db()
    assert not unused_attachment.category
    assert not unused_attachment.thread
    assert not unused_attachment.post
    assert not unused_attachment.uploader
    assert unused_attachment.is_deleted


def test_post_edit_state_schedules_post_upgrade_for_post_with_code_block(
    mock_upgrade_post_content, user_request, other_user_thread
):
    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_post_message(parse("Hello world\n[code=python]add(1, 3)[/code]"))
    state.save()

    assert state.post.id
    assert state.post.thread == state.thread

    mock_upgrade_post_content.delay.assert_called_once_with(
        state.post.id, state.post.sha256_checksum
    )


def test_post_edit_state_save_creates_thread_update_object_for_changed_title(
    user_request, user, other_user_thread
):
    original_title = other_user_thread.title

    assert not ThreadUpdate.objects.exists()

    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_thread_title("Updated title")
    state.save()

    assert ThreadUpdate.objects.count() == 1

    thread_update = ThreadUpdate.objects.first()
    assert thread_update.actor == user
    assert thread_update.action == ThreadUpdateActionName.CHANGED_TITLE
    assert thread_update.context == original_title
    assert not thread_update.context_id
    assert not thread_update.context_type


def test_post_edit_state_save_updates_context_in_existing_thread_updates(
    user_request,
    user,
    thread,
    other_user_thread,
):
    thread_update = create_split_thread_update(thread, other_user_thread, user)

    state = PostEditState(user_request, other_user_thread.first_post)
    state.set_thread_title("Updated title")
    state.save()

    thread_update.refresh_from_db()
    assert thread_update.context == "Updated title"
    assert thread_update.get_context_id("misago_threads.thread") == other_user_thread.id
