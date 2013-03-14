from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread

class ThreadRecord(models.Model):
    user = models.ForeignKey('users.User')
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey('threads.Thread')
    updated = models.DateTimeField()
    

class ForumRecord(models.Model):
    user = models.ForeignKey('users.User')
    forum = models.ForeignKey('forums.Forum')
    updated = models.DateTimeField()
    cleared = models.DateTimeField()
    
    def get_threads(self):
        threads = {}
        for thread in ThreadRecord.objects.filter(user=self.user, forum=self.forum, updated__gte=(timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH))):
            threads[thread.thread_id] = thread
        return threads


def move_forum_content_handler(sender, **kwargs):
    ForumRecord.objects.filter(forum=sender).delete()

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_reads")


def move_thread_handler(sender, **kwargs):
    ThreadRecord.objects.filter(thread=sender).delete()

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_reads")