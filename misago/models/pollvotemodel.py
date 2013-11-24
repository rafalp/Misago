from django.db import models
from misago.signals import (rename_user, move_thread,
                            move_forum_content)

class PollVote(models.Model):
    poll = models.ForeignKey('Poll', related_name="vote_set")
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    option = models.ForeignKey('PollOption', null=True, blank=True)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    user_slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)

    class Meta:
        app_label = 'misago'


def rename_user_handler(sender, **kwargs):
    PollVote.objects.filter(user=sender).update(
                                                user_name=sender.username,
                                                user_slug=sender.username_slug,
                                                )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_poll_votes")


def move_forum_content_handler(sender, **kwargs):
    PollVote.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_polls_votes")


def move_thread_handler(sender, **kwargs):
    PollVote.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_polls_votes")