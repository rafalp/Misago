from ..state import EditThreadPostState


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
