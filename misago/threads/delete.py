from ..attachments.models import Attachment
from ..edits.models import PostEdit
from ..likes.models import Like
from ..notifications.models import Notification
from ..postgres.delete import delete_all, delete_one
from .models import (
    Attachment as DeprecatedAttachment,
    Post,
    Thread,
    PostEdit as DeprecatedPostEdit,
    PostLike as DeprecatedPostLike,
)


def delete_thread(thread: Thread):
    delete_one(thread)


def delete_post(post: Post):
    thread = post.thread

    delete_all(DeprecatedAttachment, post_id=post.id)
    delete_all(DeprecatedPostEdit, post_id=post.id)
    delete_all(DeprecatedPostLike, post_id=post.id)

    delete_all(PostEdit, post_id=post.id)
    delete_all(Like, post_id=post.id)
    delete_all(Notification, post_id=post.id)

    Attachment.objects.filter(post=post).update(post=None)

    save_thread_fields = list()
    if thread.first_post_id == post.id:
        thread.first_post = None
        save_thread_fields.append("first_post")
    if thread.last_post_id == post.id:
        thread.last_post = None
        save_thread_fields.append("last_post")
    if save_thread_fields:
        thread.save(update_fields=save_thread_fields)

    delete_one(post)
