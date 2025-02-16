from ..delete import (
    delete_attachments,
    delete_categories_attachments,
    delete_posts_attachments,
    delete_threads_attachments,
    delete_users_attachments,
)


def test_delete_attachments_marks_attachments_for_deletion(
    text_attachment, image_attachment
):
    delete_attachments([text_attachment, image_attachment])

    text_attachment.refresh_from_db()
    assert text_attachment.is_deleted

    image_attachment.refresh_from_db()
    assert image_attachment.is_deleted


def test_delete_attachments_removes_attachments_relations(user_text_attachment, post):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    delete_attachments([user_text_attachment])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.uploader
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert user_text_attachment.is_deleted


def test_delete_attachments_marks_attachments_for_deletion_using_ids(
    text_attachment, image_attachment
):
    delete_attachments([text_attachment.id, image_attachment.id])

    text_attachment.refresh_from_db()
    assert text_attachment.is_deleted

    image_attachment.refresh_from_db()
    assert image_attachment.is_deleted


def test_delete_attachments_excludes_unspecified_attachments(
    text_attachment, image_attachment
):
    delete_attachments([text_attachment])

    text_attachment.refresh_from_db()
    assert text_attachment.is_deleted

    image_attachment.refresh_from_db()
    assert not image_attachment.is_deleted


def test_delete_categories_attachments_marks_attachments_for_deletion(
    user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    delete_categories_attachments([post.category])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_categories_attachments_accepts_categories_ids(
    user_text_attachment, user_image_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(post)
    user_image_attachment.save()

    delete_categories_attachments([post.category_id, post.category_id])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_categories_attachments_excludes_other_categories_attachments(
    user_text_attachment, user_image_attachment, post, other_thread, other_category
):
    other_thread.category = other_category
    other_thread.save()

    other_thread.first_post.category = other_category
    other_thread.first_post.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_categories_attachments([post.category])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert user_image_attachment.category
    assert user_image_attachment.thread
    assert user_image_attachment.post
    assert user_image_attachment.uploader
    assert not user_image_attachment.is_deleted


def test_delete_threads_attachments_marks_attachments_for_deletion(
    user_text_attachment,
    user_image_attachment,
    thread,
    post,
    other_thread,
    other_category,
):
    other_thread.category = other_category
    other_thread.save()

    other_thread.first_post.category = other_category
    other_thread.first_post.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_threads_attachments([thread, other_thread])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_threads_attachments_accepts_threads_ids(
    user_text_attachment,
    user_image_attachment,
    thread,
    post,
    other_thread,
    other_category,
):
    other_thread.category = other_category
    other_thread.save()

    other_thread.first_post.category = other_category
    other_thread.first_post.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_threads_attachments([thread.id, other_thread.id])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_threads_attachments_excludes_other_threads_attachments(
    user_text_attachment,
    user_image_attachment,
    thread,
    post,
    other_thread,
    other_category,
):
    other_thread.category = other_category
    other_thread.save()

    other_thread.first_post.category = other_category
    other_thread.first_post.save()

    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_threads_attachments([thread])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert user_image_attachment.category
    assert user_image_attachment.thread
    assert user_image_attachment.post
    assert user_image_attachment.uploader
    assert not user_image_attachment.is_deleted


def test_delete_posts_attachments_marks_attachments_for_deletion(
    user_text_attachment, user_image_attachment, thread, other_thread
):
    user_text_attachment.associate_with_post(thread.first_post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_posts_attachments([thread.first_post, other_thread.first_post])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_posts_attachments_accepts_posts_ids(
    user_text_attachment, user_image_attachment, thread, other_thread
):
    user_text_attachment.associate_with_post(thread.first_post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_posts_attachments([thread.first_post_id, other_thread.first_post_id])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert not user_image_attachment.category
    assert not user_image_attachment.thread
    assert not user_image_attachment.post
    assert not user_image_attachment.uploader
    assert user_image_attachment.is_deleted


def test_delete_posts_attachments_excludes_other_posts_attachments(
    user_text_attachment, user_image_attachment, thread, other_thread
):
    user_text_attachment.associate_with_post(thread.first_post)
    user_text_attachment.save()

    user_image_attachment.associate_with_post(other_thread.first_post)
    user_image_attachment.save()

    delete_posts_attachments([thread.first_post])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    user_image_attachment.refresh_from_db()
    assert user_image_attachment.category
    assert user_image_attachment.thread
    assert user_image_attachment.post
    assert user_image_attachment.uploader
    assert not user_image_attachment.is_deleted


def test_delete_users_attachments_marks_attachments_for_deletion(
    user, other_user, user_text_attachment, other_user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    delete_users_attachments([user, other_user])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    other_user_text_attachment.refresh_from_db()
    assert not other_user_text_attachment.category
    assert not other_user_text_attachment.thread
    assert not other_user_text_attachment.uploader
    assert not other_user_text_attachment.post
    assert other_user_text_attachment.is_deleted


def test_delete_users_attachments_accepts_users_ids(
    user, other_user, user_text_attachment, other_user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    delete_users_attachments([user.id, other_user.id])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    other_user_text_attachment.refresh_from_db()
    assert not other_user_text_attachment.category
    assert not other_user_text_attachment.thread
    assert not other_user_text_attachment.post
    assert not other_user_text_attachment.uploader
    assert other_user_text_attachment.is_deleted


def test_delete_users_attachments_excludes_other_threads_attachments(
    user, user_text_attachment, other_user_text_attachment, post
):
    user_text_attachment.associate_with_post(post)
    user_text_attachment.save()

    other_user_text_attachment.associate_with_post(post)
    other_user_text_attachment.save()

    delete_users_attachments([user])

    user_text_attachment.refresh_from_db()
    assert not user_text_attachment.category
    assert not user_text_attachment.thread
    assert not user_text_attachment.post
    assert not user_text_attachment.uploader
    assert user_text_attachment.is_deleted

    other_user_text_attachment.refresh_from_db()
    assert other_user_text_attachment.category
    assert other_user_text_attachment.thread
    assert other_user_text_attachment.post
    assert other_user_text_attachment.uploader
    assert not other_user_text_attachment.is_deleted
