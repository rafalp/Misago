from django.db import models
from misago.signals import move_thread, move_thread, move_forum_content

class PollOption(models.Model):
    poll = models.ForeignKey('Poll', related_name="option_set")
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    name = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'misago'


def move_forum_content_handler(sender, **kwargs):
    PollOption.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_polls_options")


def move_thread_handler(sender, **kwargs):
    PollOption.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_polls_options")