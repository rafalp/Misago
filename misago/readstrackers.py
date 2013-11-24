from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from misago.models import Thread, ForumRead, ThreadRead

class ForumsTracker(object):
    def __init__(self, user):
        self.user = user
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        self.forums = {}
        if user.is_authenticated() and settings.READS_TRACKER_LENGTH > 0:
            if user.join_date > self.cutoff:
                self.cutoff = user.join_date
            for forum in ForumRead.objects.filter(user=user).filter(updated__gte=self.cutoff).values('id', 'forum_id', 'updated', 'cleared'):
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
        self.need_create = None
        self.need_update = None
        self.request = request
        self.forum = forum
        self.cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)
        if request.user.is_authenticated():
            if request.user.join_date > self.cutoff:
                self.cutoff = request.user.join_date
            try:
                self.record = ForumRead.objects.get(user=request.user, forum=forum)
                if self.record.cleared > self.cutoff:
                    self.cutoff = self.record.cleared
            except ForumRead.DoesNotExist:
                self.record = ForumRead(user=request.user, forum=forum, cleared=self.cutoff)
            self.threads = self.record.get_threads()

    def read_date(self, thread):
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
                self.threads[thread.pk].updated = post.date
                self.need_update = self.threads[thread.pk]
            except KeyError:
                self.need_create = thread

    def unread_count(self, queryset=None):
        try:
            return self.unread_threads
        except AttributeError:
            self.unread_threads = 0
            if queryset == None:
                queryset = self.default_queryset()
            for thread in queryset.filter(last__gte=self.record.cleared):
                if not self.is_read(thread):
                    self.unread_threads += 1
            return self.unread_threads

    def sync(self, queryset=None):
        now = timezone.now()
        if queryset == None:
            queryset = self.default_queryset()

        if self.need_create:
            new_record = ThreadRead(
                                    user=self.request.user,
                                    thread=self.need_create,
                                    forum=self.forum,
                                    updated=now
                                    )
            new_record.save(force_insert=True)
            self.threads[new_record.thread_id] = new_record

        if self.need_update:
            self.need_update.updated = now
            self.need_update.save(force_update=True)

        if self.need_create or self.need_update:
            if not self.unread_count(queryset):
                self.record.cleared = now
            self.record.updated = now
            if self.record.pk:
                self.record.save(force_update=True)
            else:
                self.record.save(force_insert=True)

    def default_queryset(self):
        return self.request.acl.threads.filter_threads(self.request, self.forum, self.forum.thread_set)