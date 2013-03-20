from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.signals import (delete_user_content, merge_thread, move_forum_content,
                            move_thread, rename_user)
from misago.utils.strings import slugify

class ThreadManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(start__gte=start).filter(start__lte=end)

    def with_reads(self, queryset, user):
        from misago.models import ForumRead, ThreadRead

        threads = []
        threads_dict = {}
        forum_reads = {}
        cutoff = timezone.now() - timedelta(days=settings.READS_TRACKER_LENGTH)

        if user.is_authenticated() and user.join_date > cutoff:
            cutoff = user.join_date
            for row in ForumRead.objects.filter(user=user).values('forum_id', 'cleared'):
                forum_reads[row['forum_id']] = row['cleared']

        for thread in queryset:
            thread.is_read = True
            if user.is_authenticated() and thread.last > cutoff:
                try:
                    thread.is_read = thread.last <= forum_reads[thread.forum_id]
                except KeyError:
                    pass

            threads.append(thread)
            threads_dict[thread.pk] = thread

        if user.is_authenticated():
            for read in ThreadRead.objects.filter(user=user).filter(thread__in=threads_dict.keys()):
                try:
                    threads_dict[read.thread_id].is_read = (threads_dict[read.thread_id].last <= cutoff or 
                                                            threads_dict[read.thread_id].last <= read.updated or
                                                            threads_dict[read.thread_id].last <= forum_reads[read.forum_id])
                except KeyError:
                    pass

        return threads


class Thread(models.Model):
    forum = models.ForeignKey('Forum')
    weight = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    replies_reported = models.PositiveIntegerField(default=0)
    replies_moderated = models.PositiveIntegerField(default=0)
    replies_deleted = models.PositiveIntegerField(default=0)
    merges = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=30)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    start = models.DateTimeField()
    start_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    start_poster = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    start_poster_style = models.CharField(max_length=255, null=True, blank=True)
    last = models.DateTimeField()
    last_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster = models.ForeignKey('User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    moderated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    objects = ThreadManager()

    statistics_name = _('New Threads')

    class Meta:
        app_label = 'misago'

    def get_date(self):
        return self.start

    def new_start_post(self, post):
        self.start = post.date
        self.start_post = post
        self.start_poster = post.user
        self.start_poster_name = post.user.username
        self.start_poster_slug = post.user.username_slug
        if post.user.rank_id and post.user.rank.style:
            self.start_poster_style = post.user.rank.style

    def new_last_post(self, post):
        self.last = post.date
        self.last_post = post
        self.last_poster = post.user
        self.last_poster_name = post.user.username
        self.last_poster_slug = post.user.username_slug
        if post.user.rank_id and post.user.rank.style:
            self.last_poster_style = post.user.rank.style

    def move_to(self, move_to):
        move_thread.send(sender=self, move_to=move_to)
        self.forum = move_to

    def merge_with(self, thread, merge):
        merge_thread.send(sender=self, new_thread=thread, merge=merge)

    def sync(self):
        # Counters
        self.replies = self.post_set.filter(moderated=False).count() - 1
        if self.replies < 0:
            self.replies = 0
        self.replies_reported = self.post_set.filter(reported=True).count()
        self.replies_moderated = self.post_set.filter(moderated=True).count()
        self.replies_deleted = self.post_set.filter(deleted=True).count()
        # First post
        start_post = self.post_set.order_by('merge', 'id')[0:][0]
        self.start = start_post.date
        self.start_post = start_post
        self.start_poster = start_post.user
        self.start_poster_name = start_post.user_name
        self.start_poster_slug = slugify(start_post.user_name)
        self.start_poster_style = start_post.user.rank.style if start_post.user else ''
        self.upvotes = start_post.upvotes
        self.downvotes = start_post.downvotes
        # Last visible post
        if self.replies > 0:
            last_post = self.post_set.order_by('-merge', '-id').filter(moderated=False)[0:][0]
        else:
            last_post = start_post
        self.last = last_post.date
        self.last_post = last_post
        self.last_poster = last_post.user
        self.last_poster_name = last_post.user_name
        self.last_poster_slug = slugify(last_post.user_name)
        self.last_poster_style = last_post.user.rank.style if last_post.user else ''
        # Flags
        self.moderated = start_post.moderated
        self.deleted = start_post.deleted
        self.merges = last_post.merge
        
    def email_watchers(self, request, post):
        from misago.acl.builder import acl
        from misago.acl.exceptions import ACLError403, ACLError404
        from misago.models import ThreadRead

        for watch in WatchedThread.objects.filter(thread=self).filter(email=True).filter(last_read__gte=self.previous_last):
            user = watch.user
            if user.pk != request.user.pk:
                try:
                    acl = acl(request, user)
                    acl.forums.allow_forum_view(self.forum)
                    acl.threads.allow_thread_view(user, self)
                    acl.threads.allow_post_view(user, self, post)
                    if not user.is_ignoring(request.user):
                        user.email_user(
                            request,
                            'post_notification',
                            _('New reply in thread "%(thread)s"') % {'thread': self.name},
                            {'author': request.user, 'post': post, 'thread': self}
                            )
                except (ACLError403, ACLError404):
                    pass


def rename_user_handler(sender, **kwargs):
    Thread.objects.filter(start_poster=sender).update(
                                                     start_poster_name=sender.username,
                                                     start_poster_slug=sender.username_slug,
                                                     )
    Thread.objects.filter(last_poster=sender).update(
                                                     last_poster_name=sender.username,
                                                     last_poster_slug=sender.username_slug,
                                                     )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_threads")


def delete_user_content_handler(sender, **kwargs):
    for thread in Thread.objects.filter(start_poster=sender):
        thread.delete()

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_threads")


def move_forum_content_handler(sender, **kwargs):
    Thread.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads")
