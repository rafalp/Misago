from ..state import EditThreadPostState


def test_edit_thread_post_state_save_updates_thread_title(
    user_request, other_user_thread
):
    state = EditThreadPostState(user_request, other_user_thread.first_post)
    state.set_thread_title("Updated title")
    state.save()

    other_user_thread.refresh_from_db()

    assert other_user_thread.title == "Updated title"
    assert other_user_thread.slug == "updated-title"


def test_edit_thread_post_state_save_updates_post(
    user, user_request, other_user_thread
):
    state = EditThreadPostState(user_request, other_user_thread.first_post)
    state.set_post_message("Edit reply")
    state.save()

    post = other_user_thread.first_post
    post.refresh_from_db()

    assert post.original == "Edit reply"
    assert post.updated_on == state.timestamp
    assert post.edits == 1
    assert post.last_editor == user
    assert post.last_editor_name == user.username
    assert post.last_editor_slug == user.slug


def test_edit_thread_post_state_save_updates_post_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    attachment = attachment_factory(text_file, uploader=user)
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post

    state = EditThreadPostState(user_request, other_user_thread.first_post)
    state.set_post_message("Edit reply")
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


def test_edit_thread_post_state_save_deletes_post_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    attachment = attachment_factory(text_file, uploader=user, post=post)

    state = EditThreadPostState(user_request, other_user_thread.first_post)
    state.set_post_message("Edit reply")
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


def test_edit_thread_post_state_save_deletes_unused_attachments(
    user, other_user, user_request, other_user_thread, text_file, attachment_factory
):
    post = other_user_thread.first_post
    post_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    unused_attachment = attachment_factory(text_file, uploader=user)

    state = EditThreadPostState(user_request, other_user_thread.first_post)
    state.set_post_message("Edit reply")
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
