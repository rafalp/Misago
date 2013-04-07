from django.db import models
from misago.signals import (merge_post, merge_thread, move_forum_content,
                            move_post, move_thread, rename_forum, rename_user)

class Checkpoint(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    post = models.ForeignKey('Post')
    action = models.CharField(max_length=255)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    target_user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    target_user_name = models.CharField(max_length=255, null=True, blank=True)
    target_user_slug = models.CharField(max_length=255, null=True, blank=True)
    old_forum = models.ForeignKey('Forum', null=True, blank=True, related_name='+')
    old_forum_name = models.CharField(max_length=255, null=True, blank=True)
    old_forum_slug = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'misago'


def rename_forum_handler(sender, **kwargs):
    Checkpoint.objects.filter(old_forum=sender).update(
                                                  old_forum_name=sender.name,
                                                  old_forum_slug=sender.slug,
                                                  )

rename_forum.connect(rename_forum_handler, dispatch_uid="rename_forum_checkpoints")


def rename_user_handler(sender, **kwargs):
    Checkpoint.objects.filter(user=sender).update(
                                                  user_name=sender.username,
                                                  user_slug=sender.username_slug,
                                                  )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_checkpoints")


def move_forum_content_handler(sender, **kwargs):
    Checkpoint.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_checkpoints")


def move_thread_handler(sender, **kwargs):
    Checkpoint.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_checkpoints")


def merge_thread_handler(sender, **kwargs):
    Checkpoint.objects.filter(thread=sender).delete()

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_checkpoints")


def move_posts_handler(sender, **kwargs):
    if sender.checkpoints:
        prev_post = Post.objects.filter(thread=sender.thread_id).filter(merge__lte=sender.merge).exclude(id=sender.pk).order_by('merge', '-id')[:1][0]
        Checkpoint.objects.filter(post=sender).update(post=prev_post)
        prev_post.checkpoints = True
        prev_post.save(force_update=True)
    sender.checkpoints = False

move_post.connect(move_posts_handler, dispatch_uid="move_posts_checkpoints")


def merge_posts_handler(sender, **kwargs):
    Checkpoint.objects.filter(post=sender).update(post=kwargs['new_post'])
    if sender.checkpoints:
        kwargs['new_post'].checkpoints = True

merge_post.connect(merge_posts_handler, dispatch_uid="merge_posts_checkpoints")
