from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from misago.signals import move_forum_content

class ForumRead(models.Model):
    user = models.ForeignKey('User')
    forum = models.ForeignKey('Forum')
    updated = models.DateTimeField()
    cleared = models.DateTimeField()
    
    class Meta:
        app_label = 'misago'

    def get_threads(self):
        from misago.models import ThreadRead
        
        threads = {}
        for thread in ThreadRead.objects.filter(user=self.user, forum=self.forum, updated__gte=(timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH))):
            threads[thread.thread_id] = thread
        return threads


def move_forum_content_handler(sender, **kwargs):
    ForumRead.objects.filter(forum=sender).delete()
    ForumRead.objects.filter(forum=kwargs['move_to']).delete()

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_reads")