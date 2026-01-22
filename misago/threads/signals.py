from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import Signal, receiver
from django.utils.translation import pgettext

from ..attachments.delete import delete_users_attachments
from ..attachments.models import Attachment
from ..categories.models import Category
from ..edits.models import PostEdit
from ..likes.models import Like
from ..likes.synchronize import synchronize_post_likes
from ..notifications.models import Notification, WatchedThread
from ..polls.models import Poll, PollVote
from ..threadupdates.models import ThreadUpdate
from ..users.signals import (
    anonymize_user_data,
    archive_user_data,
    delete_user_content,
    username_changed,
)
from .anonymize import anonymize_post_last_likes
from .models import (
    Attachment as LegacyAttachment,
    Post,
    PostEdit as LegacyPostEdit,
    PostLike,
    Thread,
)
from .synchronize import synchronize_thread

delete_post = Signal()
delete_thread = Signal()
merge_post = Signal()
merge_thread = Signal()
move_post = Signal()
move_thread = Signal()
update_thread_title = Signal()


@receiver(delete_thread)
def delete_thread_updates(sender, **kwargs):
    ThreadUpdate.objects.filter(thread=sender).delete()


@receiver(merge_thread)
def merge_threads(sender, **kwargs):
    other_thread = kwargs["other_thread"]

    other_thread.post_set.update(category=sender.category, thread=sender)
    LegacyPostEdit.objects.filter(thread=other_thread).update(
        category=sender.category, thread=sender
    )
    PostLike.objects.filter(thread=other_thread).update(
        category=sender.category, thread=sender
    )

    other_thread.notification_set.update(
        category=sender.category,
        thread=sender,
        thread_title=sender.title,
    )

    other_thread.watchedthread_set.update(
        category=sender.category,
        thread=sender,
    )


@receiver(move_post)
def move_post_notifications(sender, **kwargs):
    sender.notification_set.update(
        category=sender.category,
        thread=sender.thread,
        thread_title=sender.thread.title,
    )


@receiver(move_thread)
def move_thread_content(sender, **kwargs):
    sender.post_set.update(category=sender.category)
    PostEdit.objects.filter(thread=sender).update(category=sender.category)
    LegacyPostEdit.objects.filter(thread=sender).update(category=sender.category)
    PostLike.objects.filter(thread=sender).update(category=sender.category)
    sender.pollvote_set.update(category=sender.category)
    sender.notification_set.update(category=sender.category)
    sender.watchedthread_set.update(category=sender.category)


@receiver(update_thread_title)
def change_thread_title(sender, **kwargs):
    sender.notification_set.update(thread_title=sender.title)


@receiver(delete_user_content)
def delete_user_threads(sender, **kwargs):
    delete_users_attachments([sender])

    recount_categories = set()
    recount_threads = set()

    Notification.objects.filter(
        Q(thread__starter=sender) | Q(post__poster=sender)
    ).delete()

    ThreadUpdate.objects.filter(actor=sender).delete()
    ThreadUpdate.objects.context_object(sender).clear_context_objects()

    WatchedThread.objects.filter(thread__starter=sender).delete()

    liked_posts = Post.objects.filter(
        id__in=Like.objects.filter(user=sender).values("post_id"),
    )
    for post in liked_posts.iterator(chunk_size=50):
        synchronize_post_likes(post, Like.objects.exclude(user=sender))

    PostEdit.objects.filter(user=sender).delete()
    LegacyPostEdit.objects.filter(editor=sender).delete()
    Like.objects.filter(user=sender).delete()

    for thread in sender.thread_set.iterator(chunk_size=50):
        recount_categories.add(thread.category_id)
        with transaction.atomic():
            thread.delete()

    for post in Post.objects.filter(poster=sender).iterator(chunk_size=50):
        with transaction.atomic():
            post.delete()

    if recount_threads:
        changed_threads_qs = Thread.objects.filter(id__in=recount_threads)
        for thread in changed_threads_qs.iterator(chunk_size=50):
            synchronize_thread(thread)

    if recount_categories:
        for category in Category.objects.filter(id__in=recount_categories):
            category.synchronize()
            category.save()


@receiver(archive_user_data)
def archive_user_attachments(sender, archive=None, **kwargs):
    queryset = Attachment.objects.filter(uploader=sender).order_by("id")
    for attachment in queryset.iterator(chunk_size=50):
        archive.add_model_file(
            attachment.upload,
            prefix=attachment.uploaded_at.strftime("%H%M%S"),
            date=attachment.uploaded_at,
        )


@receiver(archive_user_data)
def archive_user_legacy_attachments(sender, archive=None, **kwargs):
    queryset = sender.attachment_set.order_by("id")
    for attachment in queryset.iterator(chunk_size=50):
        archive.add_model_file(
            attachment.file,
            prefix=attachment.uploaded_on.strftime("%H%M%S-legacy-file"),
            date=attachment.uploaded_on,
        )
        archive.add_model_file(
            attachment.image,
            prefix=attachment.uploaded_on.strftime("%H%M%S-legacy-image"),
            date=attachment.uploaded_on,
        )
        archive.add_model_file(
            attachment.thumbnail,
            prefix=attachment.uploaded_on.strftime("%H%M%S-legacy-thumbnail"),
            date=attachment.uploaded_on,
        )


@receiver(archive_user_data)
def archive_user_posts(sender, archive=None, **kwargs):
    for post in sender.post_set.order_by("id").iterator(chunk_size=50):
        item_name = post.posted_at.strftime("%H%M%S-post")
        archive.add_text(item_name, post.parsed, date=post.posted_at)


@receiver(archive_user_data)
def archive_user_posts_edits(sender, archive=None, **kwargs):
    queryset = PostEdit.objects.filter(post__poster=sender)
    for post_edit in queryset.order_by("id").iterator(chunk_size=50):
        item_name = post_edit.edited_at.strftime("%H%M%S-post-edit")
        archive.add_text(item_name, post_edit.old_content, date=post_edit.edited_at)
    queryset = PostEdit.objects.filter(user=sender).exclude(
        id__in=queryset.values("id")
    )
    for post_edit in queryset.order_by("id").iterator(chunk_size=50):
        item_name = post_edit.edited_at.strftime("%H%M%S-post-edit")
        archive.add_text(item_name, post_edit.old_content, date=post_edit.edited_at)


@receiver(archive_user_data)
def archive_user_legacy_posts_edits(sender, archive=None, **kwargs):
    queryset = LegacyPostEdit.objects.filter(post__poster=sender)
    for post_edit in queryset.order_by("id").iterator(chunk_size=50):
        item_name = post_edit.edited_on.strftime("%H%M%S-post-edit")
        archive.add_text(item_name, post_edit.edited_from, date=post_edit.edited_on)
    queryset = LegacyPostEdit.objects.filter(editor=sender).exclude(
        id__in=queryset.values("id")
    )
    for post_edit in queryset.order_by("id").iterator(chunk_size=50):
        item_name = post_edit.edited_on.strftime("%H%M%S-post-edit")
        archive.add_text(item_name, post_edit.edited_from, date=post_edit.edited_on)


@receiver(archive_user_data)
def archive_user_polls(sender, archive=None, **kwargs):
    for poll in sender.poll_set.order_by("id").iterator(chunk_size=50):
        item_name = poll.posted_on.strftime("%H%M%S-poll")
        archive.add_dict(
            item_name,
            {
                pgettext("archived poll", "Question"): poll.question,
                pgettext("archived poll", "Choices"): ", ".join(
                    [c["label"] for c in poll.choices]
                ),
            },
            date=poll.posted_on,
        )


@receiver(archive_user_data)
def archive_user_thread_updates(sender, archive=None, **kwargs):
    queryset = ThreadUpdate.objects.filter(actor=sender).order_by("id")

    for thread_update in queryset.iterator(chunk_size=50):
        item_name = thread_update.created_at.strftime("%H%M%S-thread-update")
        archive.add_dict(
            item_name,
            {
                pgettext("archived thread update", "Action"): thread_update.action,
                pgettext("archived thread update", "Context"): thread_update.context,
            },
            date=thread_update.created_at,
        )


@receiver(archive_user_data)
def archive_user_context_thread_updates(sender, archive=None, **kwargs):
    queryset = ThreadUpdate.objects.context_object(sender).order_by("id")

    for thread_update in queryset.iterator(chunk_size=50):
        item_name = thread_update.created_at.strftime("%H%M%S-thread-update")
        archive.add_dict(
            item_name,
            {
                pgettext("archived thread update", "Action"): thread_update.action,
                pgettext("archived thread update", "Context"): thread_update.context,
            },
            date=thread_update.created_at,
        )


@receiver(anonymize_user_data)
def anonymize_user_in_thread_updates(sender, **kwargs):
    ThreadUpdate.objects.filter(actor=sender).update(actor_name=sender.username)
    ThreadUpdate.objects.filter(hidden_by=sender).update(hidden_by_name=sender.username)
    ThreadUpdate.objects.context_object(sender).update(context=sender.username)


@receiver([anonymize_user_data])
def anonymize_user_in_likes(sender, **kwargs):
    for post in sender.liked_post_set.iterator(chunk_size=50):
        anonymize_post_last_likes(sender, post)


@receiver([anonymize_user_data, username_changed])
def update_usernames(sender, **kwargs):
    Thread.objects.filter(starter=sender).update(
        starter_name=sender.username, starter_slug=sender.slug
    )

    Thread.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username, last_poster_slug=sender.slug
    )

    Thread.objects.filter(best_answer_marked_by=sender).update(
        best_answer_marked_by_name=sender.username,
        best_answer_marked_by_slug=sender.slug,
    )

    ThreadUpdate.objects.filter(actor=sender).update(actor_name=sender.username)
    ThreadUpdate.objects.filter(hidden_by=sender).update(hidden_by_name=sender.username)
    ThreadUpdate.objects.context_object(sender).update(context=sender.username)

    Post.objects.filter(poster=sender).update(poster_name=sender.username)

    Post.objects.filter(last_editor=sender).update(
        last_editor_name=sender.username, last_editor_slug=sender.slug
    )

    PostEdit.objects.filter(user=sender).update(
        user_name=sender.username, user_slug=sender.slug
    )
    LegacyPostEdit.objects.filter(editor=sender).update(
        editor_name=sender.username, editor_slug=sender.slug
    )

    Like.objects.filter(user=sender).update(
        user_name=sender.username, user_slug=sender.slug
    )

    liked_posts = Post.objects.filter(
        id__in=Like.objects.filter(user=sender).values("post_id"),
    )
    for post in liked_posts.iterator(chunk_size=50):
        update_post_last_likes = False
        for like in post.last_likes:
            if like["id"] == sender.id:
                like["username"] = sender.username
                update_post_last_likes = True
        if update_post_last_likes:
            post.save(update_fields=["last_likes"])

    Attachment.objects.filter(uploader=sender).update(
        uploader_name=sender.username, uploader_slug=sender.slug
    )
    LegacyAttachment.objects.filter(uploader=sender).update(
        uploader_name=sender.username, uploader_slug=sender.slug
    )

    Poll.objects.filter(starter=sender).update(
        starter_name=sender.username, starter_slug=sender.slug
    )

    PollVote.objects.filter(voter=sender).update(
        voter_name=sender.username, voter_slug=sender.slug
    )


@receiver(pre_delete, sender=get_user_model())
def remove_private_threads_without_members(sender, **kwargs):
    queryset = Thread.objects.filter(
        id__in=kwargs["instance"].privatethreadmember_set.values("thread_id"),
    ).order_by("-id")
    for thread in queryset.iterator(chunk_size=50):
        if thread.privatethreadmember_set.count() <= 1:
            with transaction.atomic():
                thread.delete()
