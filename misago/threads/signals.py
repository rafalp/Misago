from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import pre_delete
from django.dispatch import Signal, receiver
from django.urls import reverse

from misago.categories.models import Category
from misago.categories.signals import delete_category_content, move_category_content
from misago.core.pgutils import batch_delete, batch_update
from misago.core.utils import ANONYMOUS_IP
from misago.users.signals import anonymize_user_content, delete_user_content, username_changed

from .models import Attachment, Poll, PollVote, Post, PostEdit, PostLike, Thread


delete_post = Signal()
delete_thread = Signal()
merge_post = Signal(providing_args=["other_post"])
merge_thread = Signal(providing_args=["other_thread"])
move_post = Signal()
move_thread = Signal()


@receiver(merge_thread)
def merge_threads(sender, **kwargs):
    other_thread = kwargs['other_thread']

    other_thread.post_set.update(
        category=sender.category,
        thread=sender,
    )
    other_thread.postedit_set.update(
        category=sender.category,
        thread=sender,
    )
    other_thread.postlike_set.update(
        category=sender.category,
        thread=sender,
    )

    other_thread.subscription_set.exclude(
        user__in=sender.subscription_set.values('user'),
    ).update(
        category=sender.category,
        thread=sender,
    )


@receiver(merge_post)
def merge_posts(sender, **kwargs):
    other_post = kwargs['other_post']
    for user in sender.mentions.iterator():
        other_post.mentions.add(user)


@receiver(move_thread)
def move_thread_content(sender, **kwargs):
    sender.post_set.update(category=sender.category)
    sender.postedit_set.update(category=sender.category)
    sender.postlike_set.update(category=sender.category)
    sender.pollvote_set.update(category=sender.category)
    sender.subscription_set.update(category=sender.category)

    Poll.objects.filter(thread=sender).update(category=sender.category)


@receiver(delete_category_content)
def delete_category_threads(sender, **kwargs):
    sender.subscription_set.all().delete()
    sender.pollvote_set.all().delete()
    sender.poll_set.all().delete()
    sender.postlike_set.all().delete()
    sender.thread_set.all().delete()
    sender.postedit_set.all().delete()
    sender.post_set.all().delete()


@receiver(move_category_content)
def move_category_threads(sender, **kwargs):
    new_category = kwargs['new_category']

    sender.thread_set.update(category=new_category)
    sender.post_set.filter(category=sender).update(category=new_category)
    sender.postedit_set.filter(category=sender).update(category=new_category)
    sender.postlike_set.filter(category=sender).update(category=new_category)
    sender.poll_set.filter(category=sender).update(category=new_category)
    sender.pollvote_set.update(category=new_category)
    sender.subscription_set.update(category=new_category)


@receiver(delete_user_content)
def delete_user_threads(sender, **kwargs):
    recount_categories = set()
    recount_threads = set()

    for thread in batch_delete(sender.thread_set.all(), 50):
        recount_categories.add(thread.category_id)
        with transaction.atomic():
            thread.delete()

    for post in batch_delete(sender.post_set.all(), 50):
        recount_categories.add(post.category_id)
        recount_threads.add(post.thread_id)
        with transaction.atomic():
            post.delete()

    if recount_threads:
        changed_threads_qs = Thread.objects.filter(id__in=recount_threads)
        for thread in batch_update(changed_threads_qs, 50):
            thread.synchronize()
            thread.save()

    if recount_categories:
        for category in Category.objects.filter(id__in=recount_categories):
            category.synchronize()
            category.save()


@receiver([delete_user_content])
def delete_user_in_likes(sender, **kwargs):
    for post in sender.liked_post_set.iterator():
        cleaned_likes = list(filter(lambda i: i['id'] != sender.id, post.last_likes))
        if cleaned_likes != post.last_likes:
            post.last_likes = cleaned_likes
            post.save(update_fields=['last_likes'])


@receiver(anonymize_user_content)
def anonymize_user(sender, **kwargs):
    Post.objects.filter(poster=sender).update(poster_ip=ANONYMOUS_IP)
    PostEdit.objects.filter(editor=sender).update(editor_ip=ANONYMOUS_IP)
    PostLike.objects.filter(liker=sender).update(liker_ip=ANONYMOUS_IP)

    Attachment.objects.filter(uploader=sender).update(uploader_ip=ANONYMOUS_IP)

    Poll.objects.filter(poster=sender).update(poster_ip=ANONYMOUS_IP)
    PollVote.objects.filter(voter=sender).update(voter_ip=ANONYMOUS_IP)


@receiver(anonymize_user_content)
def anonymize_user_in_events(sender, **kwargs):
    queryset = Post.objects.filter(
        is_event=True,
        event_type__in=[
            'added_participant',
            'changed_owner',
            'owner_left',
            'removed_owner',
            'participant_left',
            'removed_participant',
        ],
        event_context__user__id=sender.id,
    ).iterator()

    for event in queryset:
        event.event_context = {
            'user': {
                'id': None,
                'username': sender.username,
                'url': reverse('misago:users'),
            },
        }
        event.save(update_fields=['event_context'])


@receiver([anonymize_user_content])
def anonymize_user_in_likes(sender, **kwargs):
    for post in sender.liked_post_set.iterator():
        cleaned_likes = []
        for like in post.last_likes:
            if like['id'] == sender.id:
                cleaned_likes.append({
                    'id': None,
                    'username': sender.username
                })
            else:
                cleaned_likes.append(like)

        if cleaned_likes != post.last_likes:
            post.last_likes = cleaned_likes
            post.save(update_fields=['last_likes'])


@receiver([anonymize_user_content, username_changed])
def update_usernames(sender, **kwargs):
    Thread.objects.filter(starter=sender).update(
        starter_name=sender.username,
        starter_slug=sender.slug,
    )

    Thread.objects.filter(last_poster=sender).update(
        last_poster_name=sender.username,
        last_poster_slug=sender.slug,
    )
    
    Thread.objects.filter(best_answer_marked_by=sender).update(
        best_answer_marked_by_name=sender.username,
        best_answer_marked_by_slug=sender.slug,
    )

    Post.objects.filter(poster=sender).update(
        poster_name=sender.username,
    )

    Post.objects.filter(last_editor=sender).update(
        last_editor_name=sender.username,
        last_editor_slug=sender.slug,
    )

    PostEdit.objects.filter(editor=sender).update(
        editor_name=sender.username,
        editor_slug=sender.slug,
    )

    PostLike.objects.filter(liker=sender).update(
        liker_name=sender.username,
        liker_slug=sender.slug,
    )

    Attachment.objects.filter(uploader=sender).update(
        uploader_name=sender.username,
        uploader_slug=sender.slug,
    )

    Poll.objects.filter(poster=sender).update(
        poster_name=sender.username,
        poster_slug=sender.slug,
    )

    PollVote.objects.filter(voter=sender).update(
        voter_name=sender.username,
        voter_slug=sender.slug,
    )


@receiver(pre_delete, sender=get_user_model())
def remove_unparticipated_private_threads(sender, **kwargs):
    threads_qs = kwargs['instance'].privatethread_set.all()
    for thread in batch_update(threads_qs, 50):
        if thread.participants.count() == 1:
            with transaction.atomic():
                thread.delete()
