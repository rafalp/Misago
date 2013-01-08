from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from misago.readstracker.models import Record
from misago.threads.models import Thread

class ForumsTracker(object):
    def __init__(self, user):
        self.user = user
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        self.forums = {}
        if self.user.is_authenticated() and settings.READS_TRACKER_LENGTH > 0:
            for forum in Record.objects.filter(user=user).filter(updated__gte=self.cutoff).values('id', 'forum_id', 'updated', 'cleared'):
                 self.forums[forum['forum_id']] = forum
                 
    def is_read(self, forum):
        if not self.user.is_authenticated() or not forum.last_thread_date:
            return True
        try:
            return forum.last_thread_date <= self.cutoff or forum.last_thread_date <= self.forums[forum.pk]['cleared']
        except KeyError:
            return False


class ThreadsTracker(object):
    def __init__(self, request, forum):
        self.need_sync = False
        self.need_update = False
        self.request = request
        self.forum = forum
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        if request.user.is_authenticated():
            try:
                self.record = Record.objects.get(user=request.user,forum=forum)
                if self.record.cleared > self.cutoff:
                    self.cutoff = self.record.cleared
            except Record.DoesNotExist:
                self.record = Record(user=request.user,forum=forum,cleared=self.cutoff)
            self.threads = self.record.get_threads()
    
    def get_read_date(self, thread):
        if not self.request.user.is_authenticated():
            return timezone.now()
        try:
            if self.threads[thread.pk] > self.cutoff:
                return self.threads[thread.pk]
        except KeyError:
            pass
        return self.cutoff
        
    def is_read(self, thread):
        if not self.request.user.is_authenticated():
            return True
        try:
            if thread.last <= self.cutoff and thread.pk in self.threads:
                del self.threads[thread.pk]
                self.need_update = True
            return thread.last <= self.cutoff or thread.last <= self.threads[thread.pk]
        except KeyError:
            return False
        
    def set_read(self, thread, post):
        if self.request.user.is_authenticated():
            try:
                if self.threads[thread.pk] < post.date:
                    self.threads[thread.pk] = post.date
                    self.need_sync = True
            except KeyError:
                self.threads[thread.pk] = post.date
                self.need_sync = True
                        
    def sync(self):
        now = timezone.now()
        if self.need_sync:
            unread_threads = 0
            for thread in self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set.filter(last__gte=self.record.cleared)):
                if not self.is_read(thread):
                    unread_threads += 1
            if not unread_threads:
                self.record.cleared = now
                
        if self.need_sync or self.need_update:
            self.record.updated = now
            self.record.set_threads(self.threads)
            self.record.save(force_update=self.record.pk)