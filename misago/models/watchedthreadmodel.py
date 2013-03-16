from django.db import models
from misago.forums.signals import 
from misago.signals import merge_thread, move_forum_content, move_thread

class WatchedThread(models.Model):
    user = models.ForeignKey('User')
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    last_read = models.DateTimeField()
    email = models.BooleanField(default=False)
    deleted = False

    class Meta:
        app_label = 'misago'
    
    def save(self, *args, **kwargs):
        if not self.deleted:
            super(WatchedThread, self).save(*args, **kwargs)
            

def move_forum_content_handler(sender, **kwargs):
    WatchedThread.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_watchers")


def move_thread_handler(sender, **kwargs):
    WatchedThread.objects.filter(forum=sender.forum_id).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_watchers")


def merge_thread_handler(sender, **kwargs):
    WatchedThread.objects.filter(thread=sender).delete()

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_watchers")