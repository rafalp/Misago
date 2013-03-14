from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from misago.readstracker.models import ForumRecord, ThreadRecord
from misago.threads.models import Thread

class ForumsTracker(object):
    def __init__(self, user):
        self.user = user
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        self.forums = {}
        if user.is_authenticated() and settings.READS_TRACKER_LENGTH > 0:
            if user.join_date > self.cutoff:
                self.cutoff = user.join_date
            for forum in ForumRecord.objects.filter(user=user).filter(updated__gte=self.cutoff).values('id', 'forum_id', 'updated', 'cleared'):
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
        self.need_create = []
        self.need_update = []
        self.need_delete = []
        self.request = request
        self.forum = forum
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        if request.user.is_authenticated():
            if request.user.join_date > self.cutoff:
                self.cutoff = request.user.join_date
            try:
                self.record = ForumRecord.objects.get(user=request.user, forum=forum)
                if self.record.cleared > self.cutoff:
                    self.cutoff = self.record.cleared
            except ForumRecord.DoesNotExist:
                self.record = ForumRecord(user=request.user, forum=forum, cleared=self.cutoff)
            self.threads = self.record.get_threads()

    def get_read_date(self, thread):
        if not self.request.user.is_authenticated():
            return timezone.now()
        try:
            if self.threads[thread.pk].updated > self.cutoff:
                return self.threads[thread.pk].updated
        except KeyError:
            pass
        return self.cutoff

    def is_read(self, thread):
        if not self.request.user.is_authenticated():
            return True
        try:
            return thread.last <= self.cutoff or thread.last <= self.threads[thread.pk].updated
        except KeyError:
            return False

    def set_read(self, thread, post):
        if self.request.user.is_authenticated() and post.date > self.cutoff:
            try:
                if self.threads[thread.pk].updated < post.date:
                    self.need_update.append(thread.pk)
                self.threads[thread.pk].updated = post.date
            except KeyError:
                self.need_create.append(thread)

    def sync(self):
        now = timezone.now()

        if self.need_create:
            ThreadRecord.objects.bulk_create(
                [ThreadRecord(user=self.request.user, thread=t, forum=self.forum, updated=now) for t in self.need_create])

        if self.need_update:
            ThreadRecord.objects.filter(user_id=self.request.user.id).filter(thread_id__in=self.need_update).update(updated=now)

        if self.need_create or self.need_delete or self.need_update:
            unread_threads = 0
            for thread in self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set.filter(last__gte=self.record.cleared)):
                if not self.is_read(thread):
                    unread_threads += 1
            if not unread_threads:
                self.record.cleared = now
            self.record.updated = now
            self.record.save(force_update=self.record.pk)
