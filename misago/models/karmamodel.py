from django.db import models
from misago.signals import (merge_post, merge_thread, move_forum_content,
                            move_post, move_thread, rename_user)

class Karma(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    post = models.ForeignKey('Post')
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    score = models.IntegerField(default=0)

    class Meta:
        app_label = 'misago'


def rename_user_handler(sender, **kwargs):
    Karma.objects.filter(user=sender).update(
                                             user_name=sender.username,
                                             user_slug=sender.username_slug,
                                             )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_karmas")


def move_forum_content_handler(sender, **kwargs):
    Karma.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_karmas")


def move_thread_handler(sender, **kwargs):
    Karma.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_karmas")


def merge_thread_handler(sender, **kwargs):
    Karma.objects.filter(thread=sender).update(thread=kwargs['new_thread'])

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_karmas")


def move_posts_handler(sender, **kwargs):
    Karma.objects.filter(post=sender).update(forum=kwargs['move_to'].forum, thread=kwargs['move_to'])

move_post.connect(move_posts_handler, dispatch_uid="move_posts_karmas")


def merge_posts_handler(sender, **kwargs):
    Karma.objects.filter(post=sender).update(post=kwargs['new_post'])
    kwargs['new_post'].upvotes += self.upvotes
    kwargs['new_post'].downvotes += self.downvotes
    kwargs['new_post'].score += self.score

merge_post.connect(merge_posts_handler, dispatch_uid="merge_posts_karmas")
