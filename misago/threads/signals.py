from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import Signal, receiver
from django.utils.translation import pgettext

from ..attachments.delete import delete_users_attachments
from ..attachments.models import Attachment
from ..categories.models import Category
from ..notifications.models import Notification, WatchedThread
from ..users.signals import (
    anonymize_user_data,
    archive_user_data,
    delete_user_content,
    username_changed,
)
from .anonymize import ANONYMIZABLE_EVENTS, anonymize_event, anonymize_post_last_likes
from .models import (
    Attachment as LegacyAttachment,
    Poll,
    PollVote,
    Post,
    PostEdit,
    PostLike,
    Thread,
)

delete_post = Signal()
delete_thread = Signal()
merge_post = Signal()
merge_thread = Signal()
move_post = Signal()
move_thread = Signal()
update_thread_title = Signal()


@receiver(merge_thread)
def merge_threads(sender, **kwargs):
    other_thread = kwargs["other_thread"]

    other_thread.post_set.update(category=sender.category, thread=sender)
    other_thread.postedit_set.update(category=sender.category, thread=sender)
    other_thread.postlike_set.update(category=sender.category, thread=sender)

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
    sender.postedit_set.update(category=sender.category)
    sender.postlike_set.update(category=sender.category)
    sender.pollvote_set.update(category=sender.category)
    sender.notification_set.update(category=sender.category)
    sender.watchedthread_set.update(category=sender.category)

    Poll.objects.filter(thread=sender).update(category=sender.category)


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

    WatchedThread.objects.filter(thread__starter=sender).delete()

    for post in sender.liked_post_set.iterator(chunk_size=50):
        cleaned_likes = list(filter(lambda i: i["id"] != sender.id, post.last_likes))
        if cleaned_likes != post.last_likes:
            post.last_likes = cleaned_likes
            post.save(update_fields=["last_likes"])

    for thread in sender.thread_set.iterator(chunk_size=50):
        recount_categories.add(thread.category_id)
        with transaction.atomic():
            thread.delete()

    for post in sender.post_set.iterator(chunk_size=50):
        recount_categories.add(post.category_id)
        recount_threads.add(post.thread_id)
        with transaction.atomic():
            post.delete()

    if recount_threads:
        changed_threads_qs = Thread.objects.filter(id__in=recount_threads)
        for thread in changed_threads_qs.iterator(chunk_size=50):
            thread.synchronize()
            thread.save()

    if recount_categories:
        for category in Category.objects.filter(id__in=recount_categories):
            category.synchronize()
            category.save()


@receiver(archive_user_data)
def archive_user_attachments(sender, archive=None, **kwargs):
    queryset = Attachment.objects.filter(uploader=sender).order_by("id")
    for attachment in queryset.iterator(chunk_size=50):
        archive.add_model_file(
            attachment.file,
            prefix=attachment.uploaded_on.strftime("%H%M%S-file"),
            date=attachment.uploaded_on,
        )
        archive.add_model_file(
            attachment.video,
            prefix=attachment.uploaded_on.strftime("%H%M%S-video"),
            date=attachment.uploaded_on,
        )
        archive.add_model_file(
            attachment.image,
            prefix=attachment.uploaded_on.strftime("%H%M%S-image"),
            date=attachment.uploaded_on,
        )
        archive.add_model_file(
            attachment.thumbnail,
            prefix=attachment.uploaded_on.strftime("%H%M%S-thumbnail"),
            date=attachment.uploaded_on,
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
        item_name = post.posted_on.strftime("%H%M%S-post")
        archive.add_text(item_name, post.parsed, date=post.posted_on)


@receiver(archive_user_data)
def archive_user_posts_edits(sender, archive=None, **kwargs):
    queryset = PostEdit.objects.filter(post__poster=sender)
    for post_edit in queryset.order_by("id").iterator(chunk_size=50):
        item_name = post_edit.edited_on.strftime("%H%M%S-post-edit")
        archive.add_text(item_name, post_edit.edited_from, date=post_edit.edited_on)
    queryset = sender.postedit_set.exclude(id__in=queryset.values("id"))
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


@receiver(anonymize_user_data)
def anonymize_user_in_events(sender, **kwargs):
    queryset = Post.objects.filter(
        is_event=True,
        event_type__in=ANONYMIZABLE_EVENTS,
        event_context__user__id=sender.id,
    )

    for event in queryset.iterator(chunk_size=50):
        anonymize_event(sender, event)


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

    Post.objects.filter(poster=sender).update(poster_name=sender.username)

    Post.objects.filter(last_editor=sender).update(
        last_editor_name=sender.username, last_editor_slug=sender.slug
    )

    PostEdit.objects.filter(editor=sender).update(
        editor_name=sender.username, editor_slug=sender.slug
    )

    PostLike.objects.filter(liker=sender).update(
        liker_name=sender.username, liker_slug=sender.slug
    )

    Attachment.objects.filter(uploader=sender).update(
        uploader_name=sender.username, uploader_slug=sender.slug
    )
    LegacyAttachment.objects.filter(uploader=sender).update(
        uploader_name=sender.username, uploader_slug=sender.slug
    )

    Poll.objects.filter(poster=sender).update(
        poster_name=sender.username, poster_slug=sender.slug
    )

    PollVote.objects.filter(voter=sender).update(
        voter_name=sender.username, voter_slug=sender.slug
    )


@receiver(pre_delete, sender=get_user_model())
def remove_private_threads_without_participants(sender, **kwargs):
    threads_qs = kwargs["instance"].privatethread_set
    for thread in threads_qs.iterator(chunk_size=50):
        if thread.participants.count() <= 1:
            with transaction.atomic():
                thread.delete()
