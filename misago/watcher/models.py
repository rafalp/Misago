from django.db import models
from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread, merge_thread

class ThreadWatch(models.Model):
    user = models.ForeignKey('users.User')
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey('threads.Thread')
    last_read = models.DateTimeField()
    email = models.BooleanField(default=False)
    deleted = False
    
    def save(self, *args, **kwargs):
        if not self.deleted:
            super(ThreadWatch, self).save(*args, **kwargs)
            

def move_forum_content_handler(sender, **kwargs):
    ThreadWatch.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_watchers")


def move_thread_handler(sender, **kwargs):
    ThreadWatch.objects.filter(forum=sender.forum_id).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_watchers")


def merge_thread_handler(sender, **kwargs):
    ThreadWatch.objects.filter(thread=sender).delete()

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_watchers")