from ..create import create_post_edit


def test_create_post_edit_creates_post_edit_by_user(user, post):
    post_edit = create_post_edit(post=post, user=user, old_content="Lorem ipsum dolor")

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user == user
    assert post_edit.user_name == user.username
    assert post_edit.user_slug == user.slug
    assert post_edit.edit_reason is None
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == []
    assert post_edit.attachments_added == 0
    assert post_edit.attachments_removed == 0


def test_create_post_edit_creates_post_edit_by_deleted_user(post):
    post_edit = create_post_edit(
        post=post, user="DeletedUser", old_content="Lorem ipsum dolor"
    )

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user is None
    assert post_edit.user_name == "DeletedUser"
    assert post_edit.user_slug == "deleteduser"
    assert post_edit.edit_reason is None
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == []
    assert post_edit.attachments_added == 0
    assert post_edit.attachments_removed == 0


def test_create_post_edit_creates_post_edit_with_edit_reason(user, post):
    post_edit = create_post_edit(
        post=post, user=user, edit_reason="Test edit", old_content="Lorem ipsum dolor"
    )

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user == user
    assert post_edit.user_name == user.username
    assert post_edit.user_slug == user.slug
    assert post_edit.edit_reason == "Test edit"
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == []
    assert post_edit.attachments_added == 0
    assert post_edit.attachments_removed == 0


def test_create_post_edit_creates_post_edit_with_new_attachment(
    user, post, user_image_attachment
):
    post_edit = create_post_edit(
        post=post,
        user=user,
        attachments=[user_image_attachment],
        old_content="Lorem ipsum dolor",
    )

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user == user
    assert post_edit.user_name == user.username
    assert post_edit.user_slug == user.slug
    assert post_edit.edit_reason is None
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == [
        {
            "id": user_image_attachment.id,
            "uploader": user.id,
            "uploader_name": user.username,
            "uploader_slug": user.slug,
            "uploaded_at": user_image_attachment.uploaded_at.isoformat(),
            "name": user_image_attachment.name,
            "filetype_id": user_image_attachment.filetype_id,
            "dimensions": [200, 200],
            "thumbnail": None,
            "size": user_image_attachment.size,
            "change": "+",
        },
    ]
    assert post_edit.attachments_added == 1
    assert post_edit.attachments_removed == 0


def test_create_post_edit_creates_post_edit_with_unchanged_attachment(
    user, post, user_image_attachment
):
    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    post_edit = create_post_edit(
        post=post,
        user=user,
        attachments=[user_image_attachment],
        old_content="Lorem ipsum dolor",
    )

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user == user
    assert post_edit.user_name == user.username
    assert post_edit.user_slug == user.slug
    assert post_edit.edit_reason is None
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == [
        {
            "id": user_image_attachment.id,
            "uploader": user.id,
            "uploader_name": user.username,
            "uploader_slug": user.slug,
            "uploaded_at": user_image_attachment.uploaded_at.isoformat(),
            "name": user_image_attachment.name,
            "filetype_id": user_image_attachment.filetype_id,
            "dimensions": [200, 200],
            "thumbnail": None,
            "size": user_image_attachment.size,
            "change": "=",
        },
    ]
    assert post_edit.attachments_added == 0
    assert post_edit.attachments_removed == 0


def test_create_post_edit_creates_post_edit_with_deleted_attachment(
    user, post, user_image_attachment
):
    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    post_edit = create_post_edit(
        post=post,
        user=user,
        deleted_attachments=[user_image_attachment],
        old_content="Lorem ipsum dolor",
    )

    assert post_edit.category == post.category
    assert post_edit.thread == post.thread
    assert post_edit.post == post
    assert post_edit.user == user
    assert post_edit.user_name == user.username
    assert post_edit.user_slug == user.slug
    assert post_edit.edit_reason is None
    assert post_edit.original_old == "Lorem ipsum dolor"
    assert post_edit.original_new == post.original
    assert post_edit.original_added == 1
    assert post_edit.original_removed == 1
    assert post_edit.attachments == [
        {
            "id": user_image_attachment.id,
            "uploader": user.id,
            "uploader_name": user.username,
            "uploader_slug": user.slug,
            "uploaded_at": user_image_attachment.uploaded_at.isoformat(),
            "name": user_image_attachment.name,
            "filetype_id": user_image_attachment.filetype_id,
            "dimensions": [200, 200],
            "thumbnail": None,
            "size": user_image_attachment.size,
            "change": "-",
        },
    ]
    assert post_edit.attachments_added == 0
    assert post_edit.attachments_removed == 1


def test_create_post_edit_doesnt_save_edit_if_commit_is_false(
    django_assert_num_queries, user, post
):
    with django_assert_num_queries(0):
        post_edit = create_post_edit(
            post=post, user=user, old_content="Lorem ipsum dolor", commit=False
        )

    assert not post_edit.id
