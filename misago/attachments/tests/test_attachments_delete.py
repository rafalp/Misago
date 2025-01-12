from ..delete import (
    delete_attachments,
    delete_categories_attachments,
    delete_posts_attachments,
    delete_threads_attachments,
    delete_users_attachments,
)


def test_delete_attachments_marks_attachments_for_deletion(
    user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    other_attachment = attachment_factory(text_file, uploader=user)

    delete_attachments([attachment, other_attachment])

    attachment.refresh_from_db()
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.is_deleted


def test_delete_attachments_marks_attachments_ids(user, text_file, attachment_factory):
    attachment = attachment_factory(text_file, uploader=user)
    other_attachment = attachment_factory(text_file, uploader=user)

    delete_attachments([attachment.id, other_attachment.id])

    attachment.refresh_from_db()
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.is_deleted


def test_delete_attachments_excludes_unspecified_attachments(
    user, text_file, attachment_factory
):
    attachment = attachment_factory(text_file, uploader=user)
    other_attachment = attachment_factory(text_file, uploader=user)

    delete_attachments([attachment])

    attachment.refresh_from_db()
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.is_deleted


def test_delete_categories_attachments_marks_attachments_for_deletion(
    user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(text_file, uploader=user, post=post)

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_categories_attachments([post.category])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_categories_attachments_accepts_categories_ids(
    user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(text_file, uploader=user, post=post)

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_categories_attachments([post.category_id, post.category_id])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_categories_attachments_excludes_other_categories_attachments(
    user, text_file, attachment_factory, post, other_thread, other_category
):
    other_thread.category = other_category
    other_thread.save()

    other_thread.first_post.category = other_category
    other_thread.first_post.save()

    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_categories_attachments([post.category])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert not other_attachment.is_deleted


def test_delete_threads_attachments_marks_attachments_for_deletion(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_threads_attachments([thread, other_thread])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_threads_attachments_accepts_threads_ids(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_threads_attachments([thread.id, other_thread.id])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_threads_attachments_excludes_other_threads_attachments(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_threads_attachments([thread])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert not other_attachment.is_deleted


def test_delete_posts_attachments_marks_attachments_for_deletion(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_posts_attachments([thread.first_post, other_thread.first_post])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_posts_attachments_accepts_posts_ids(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_posts_attachments([thread.first_post_id, other_thread.first_post_id])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert other_attachment.is_deleted


def test_delete_posts_attachments_excludes_other_threads_attachments(
    user, text_file, attachment_factory, thread, other_thread
):
    attachment = attachment_factory(text_file, uploader=user, post=thread.first_post)
    other_attachment = attachment_factory(
        text_file, uploader=user, post=other_thread.first_post
    )

    assert attachment.category
    assert attachment.thread
    assert attachment.post

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post

    delete_posts_attachments([thread.first_post])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert not other_attachment.is_deleted


def test_delete_users_attachments_marks_attachments_for_deletion(
    user, other_user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    assert attachment.category
    assert attachment.thread
    assert attachment.post
    assert attachment.uploader

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert other_attachment.uploader

    delete_users_attachments([user, other_user])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert not attachment.uploader
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert not other_attachment.uploader
    assert other_attachment.is_deleted


def test_delete_users_attachments_accepts_users_ids(
    user, other_user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    assert attachment.category
    assert attachment.thread
    assert attachment.post
    assert attachment.uploader

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert other_attachment.uploader

    delete_users_attachments([user.id, other_user.id])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert not attachment.uploader
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert not other_attachment.category
    assert not other_attachment.thread
    assert not other_attachment.post
    assert not other_attachment.uploader
    assert other_attachment.is_deleted


def test_delete_users_attachments_excludes_other_threads_attachments(
    user, other_user, text_file, attachment_factory, post
):
    attachment = attachment_factory(text_file, uploader=user, post=post)
    other_attachment = attachment_factory(text_file, uploader=other_user, post=post)

    assert attachment.category
    assert attachment.thread
    assert attachment.post
    assert attachment.uploader

    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert other_attachment.uploader

    delete_users_attachments([user])

    attachment.refresh_from_db()
    assert not attachment.category
    assert not attachment.thread
    assert not attachment.post
    assert not attachment.uploader
    assert attachment.is_deleted

    other_attachment.refresh_from_db()
    assert other_attachment.category
    assert other_attachment.thread
    assert other_attachment.post
    assert other_attachment.uploader
    assert not other_attachment.is_deleted
