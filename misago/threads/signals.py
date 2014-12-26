from django.db import transaction
from django.dispatch import receiver, Signal

from misago.core.pgutils import batch_update, batch_delete
from misago.forums.models import Forum

from misago.threads.models import Thread, Post, Event, Label


delete_post = Signal()
delete_thread = Signal()
merge_post = Signal()
merge_thread = Signal(providing_args=["other_thread"])
move_post = Signal()
move_thread = Signal()
remove_thread_participant = Signal(providing_args=["user"])


"""
Signal handlers
"""
@receiver(merge_thread)
def merge_threads_posts(sender, **kwargs):
    other_thread = kwargs['other_thread']
    other_thread.post_set.update(forum=sender.forum, thread=sender)


@receiver(move_thread)
def move_thread_content(sender, **kwargs):
    sender.post_set.update(forum=sender.forum)
    sender.event_set.update(forum=sender.forum)

    # remove unavailable labels
    if sender.label_id:
        new_forum_labels = Label.objects.get_forum_labels(sender.forum)
        if sender.label_id not in [l.pk for l in new_forum_labels]:
            sender.label = None


from misago.forums.signals import delete_forum_content, move_forum_content
@receiver(delete_forum_content)
def delete_forum_threads(sender, **kwargs):
    sender.event_set.all().delete()
    sender.thread_set.all().delete()
    sender.post_set.all().delete()


@receiver(move_forum_content)
def move_forum_threads(sender, **kwargs):
    new_forum = kwargs['new_forum']
    Thread.objects.filter(forum=sender).update(forum=new_forum)
    Post.objects.filter(forum=sender).update(forum=new_forum)
    Event.objects.filter(forum=sender).update(forum=new_forum)

    # move labels
    old_forum_labels = Label.objects.get_forum_labels(sender)
    new_forum_labels = Label.objects.get_forum_labels(new_forum)

    for label in old_forum_labels:
        if label not in new_forum_labels:
            label.forums.add(new_forum_labels)


from misago.users.signals import delete_user_content, username_changed
@receiver(delete_user_content)
def delete_user_threads(sender, **kwargs):
    recount_forums = set()
    recount_threads = set()

    for thread in batch_delete(sender.thread_set.all(), 50):
        recount_forums.add(thread.forum_id)
        with transaction.atomic():
            thread.delete()

    for post in batch_delete(sender.post_set.all(), 50):
        recount_forums.add(post.forum_id)
        recount_threads.add(post.thread_id)
        with transaction.atomic():
            post.delete()

    if recount_threads:
        changed_threads_qs = Thread.objects.filter(id__in=recount_threads)
        for thread in batch_update(changed_threads_qs, 50):
            thread.synchronize()
            thread.save()

    if recount_forums:
        for forum in Forum.objects.filter(id__in=recount_forums):
            forum.synchronize()
            forum.save()


@receiver(username_changed)
def update_usernames(sender, **kwargs):
    Thread.objects.filter(starter=sender).update(
        starter_name=sender.username,
        starter_slug=sender.slug)
    Thread.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username,
        last_poster_slug=sender.slug)

    Post.objects.filter(poster=sender).update(poster_name=sender.username)
    Post.objects.filter(last_editor=sender).update(
        last_editor_name=sender.username,
        last_editor_slug=sender.slug)

    Event.objects.filter(author=sender).update(
        author_name=sender.username,
        author_slug=sender.slug)


from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete
@receiver(pre_delete, sender=get_user_model())
def remove_unparticipated_private_threads(sender, **kwargs):
    threads_qs = kwargs['instance'].private_thread_set.all()
    for thread in batch_update(threads_qs, 50):
        if thread.participants.count() == 1:
            with transaction.atomic():
                thread.delete()
