from django.db import models
from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread

class ThreadRecord(models.Model):
    user = models.ForeignKey('User')
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    updated = models.DateTimeField()

    class Meta:
        app_label = 'misago'


def move_forum_content_handler(sender, **kwargs):
    ThreadRecord.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_reads")


def move_thread_handler(sender, **kwargs):
    ThreadRecord.objects.filter(thread=sender).delete()

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_reads")