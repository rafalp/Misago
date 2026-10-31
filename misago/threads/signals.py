from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import Signal, receiver
from django.utils.translation import pgettext


from ..attachments.models import Attachment
from ..postedits.models import PostEdit
from ..threadevents.models import ThreadEvent
from ..users.signals import (
    archive_user_data,
    username_changed,
)

from .utils import update_usernames as update_usernames_util

delete_post = Signal()
delete_thread = Signal()
merge_post = Signal()
merge_thread = Signal()
move_post = Signal()
move_thread = Signal()
update_thread_title = Signal()


@receiver(delete_thread)
def delete_thread_events(sender, **kwargs):
    ThreadEvent.objects.filter(thread=sender).delete()


@receiver(merge_thread)
def merge_threads(sender, **kwargs):
    other_thread = kwargs["other_thread"]

    other_thread.post_set.update(category=sender.category, thread=sender)

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
    sender.pollvote_set.update(category=sender.category)
    sender.notification_set.update(category=sender.category)
    sender.watchedthread_set.update(category=sender.category)


@receiver(update_thread_title)
def change_thread_title(sender, **kwargs):
    sender.notification_set.update(thread_title=sender.title)



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
def archive_user_posts(sender, archive=None, **kwargs):
    for post in sender.post_set.order_by("id").iterator(chunk_size=50):
        item_name = post.posted_at.strftime("%H%M%S-post")
        archive.add_text(item_name, post.content_parsed, date=post.posted_at)


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
def archive_user_thread_events(sender, archive=None, **kwargs):
    queryset = ThreadEvent.objects.filter(actor=sender).order_by("id")

    for thread_event in queryset.iterator(chunk_size=50):
        item_name = thread_event.created_at.strftime("%H%M%S-thread-event")
        archive.add_dict(
            item_name,
            {
                pgettext("archived thread event", "Action"): thread_event.event_type,
                pgettext("archived thread event", "Detail"): thread_event.detail,
            },
            date=thread_event.created_at,
        )


@receiver(archive_user_data)
def archive_user_content_object_thread_events(sender, archive=None, **kwargs):
    queryset = ThreadEvent.objects.content_object(sender).order_by("id")

    for thread_event in queryset.iterator(chunk_size=50):
        item_name = thread_event.created_at.strftime("%H%M%S-thread-event")
        archive.add_dict(
            item_name,
            {
                pgettext("archived thread event", "Action"): thread_event.event_type,
                pgettext("archived thread event", "Detail"): thread_event.detail,
            },
            date=thread_event.created_at,
        )


@receiver(username_changed)
def update_usernames(sender, **kwargs):
    update_usernames_util(sender)