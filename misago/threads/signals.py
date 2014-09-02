import django.dispatch
from django.dispatch import receiver

from misago.core.pgutils import batch_update, batch_delete
from misago.forums.models import Forum

from misago.threads.models import Thread, Post


delete_post = django.dispatch.Signal()
delete_thread = django.dispatch.Signal()
merge_post = django.dispatch.Signal()
merge_thread = django.dispatch.Signal()
move_post = django.dispatch.Signal()
move_thread = django.dispatch.Signal()


"""
Signal handlers
"""
@receiver(merge_thread)
def merge_threads_posts(sender, **kwargs):
    other_thread = kwargs['other_thread']
    other_thread.post_set.update(forum=sender.forum, thread=sender)


@receiver(move_thread)
def move_thread_posts(sender, **kwargs):
    sender.post_set.update(forum=sender.forum)


from misago.forums.signals import delete_forum_content, move_forum_content
@receiver(delete_forum_content)
def delete_forum_threads(sender, **kwargs):
    sender.thread_set.all().delete()
    sender.post_set.all().delete()


@receiver(move_forum_content)
def move_forum_threads(sender, **kwargs):
    new_forum = kwargs['new_forum']
    Thread.objects.filter(forum=sender).update(forum=new_forum)
    Post.objects.filter(forum=sender).update(forum=new_forum)


from misago.users.signals import delete_user_content, username_changed
@receiver(delete_user_content)
def delete_user_threads(sender, **kwargs):
    recount_forums = set()
    recount_threads = set()

    for thread in batch_delete(sender.thread_set.all(), 50):
        recount_forums.add(thread.forum_id)
        thread.delete()

    for post in batch_delete(sender.post_set.all(), 50):
        recount_forums.add(post.forum_id)
        recount_threads.add(post.thread_id)
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
