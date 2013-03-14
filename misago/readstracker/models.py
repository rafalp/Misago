from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

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