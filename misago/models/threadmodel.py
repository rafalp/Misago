from datetime import timedelta
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.signals import (delete_user_content, merge_thread, move_forum_content,
                            move_thread, rename_user, sync_user_profile, remove_thread_prefix)
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
    prefix = models.ForeignKey('ThreadPrefix', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    replies_reported = models.PositiveIntegerField(default=0)
    replies_moderated = models.PositiveIntegerField(default=0)
    replies_deleted = models.PositiveIntegerField(default=0)
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
    participants = models.ManyToManyField('User', related_name='private_thread_set')
    report_for = models.ForeignKey('Post', related_name='report_set', null=True, blank=True, on_delete=models.SET_NULL)
    has_poll = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    objects = ThreadManager()

    statistics_name = _('New Threads')

    class Meta:
        app_label = 'misago'

    @property
    def timeline_date(self):
        return self.start

    @property
    def poll(self):
        if self.has_poll:
            return self.poll_of
        else:
            return None

    def delete(self, *args, **kwargs):
        """
        FUGLY HAX for weird stuff that happens with
        relations on model deletion in MySQL
        """
        if self.replies_reported:
            clear_reports = [post.pk for post in self.post_set.filter(reported=True)]
            if clear_reports:
                Thread.objects.filter(report_for__in=clear_reports).update(report_for=None)
        return super(Thread, self).delete(*args, **kwargs)

    def get_date(self):
        return self.start

    def add_checkpoints_to_posts(self, show_all, posts, start=None, stop=None):
        qs = self.checkpoint_set.all()
        if start:
            qs = qs.filter(date__gte=start)
        if stop:
            qs = qs.filter(date__lte=stop)
        if not show_all:
            qs = qs.filter(deleted=False)
        checkpoints = [i for i in qs]

        i_max = len(posts) - 1
        for i, post in enumerate(posts):
            post.checkpoints_visible = []
            for c in checkpoints:
                if ((i == 0 and c.date <= post.date)
                        or (c.date >= post.date and (i == i_max or c.date < posts[i+1].date))):
                    post.checkpoints_visible.append(c)

    def set_checkpoint(self, request, action, user=None, forum=None, extra=None):
        if request.user.is_authenticated():
            self.checkpoint_set.create(
                                       forum=self.forum,
                                       thread=self,
                                       action=action,
                                       extra=extra,
                                       user=request.user,
                                       user_name=request.user.username,
                                       user_slug=request.user.username_slug,
                                       date=timezone.now(),
                                       ip=request.session.get_ip(request),
                                       agent=request.META.get('HTTP_USER_AGENT'),
                                       target_user=user,
                                       target_user_name=(user.username if user else None),
                                       target_user_slug=(user.username_slug if user else None),
                                       old_forum=forum,
                                       old_forum_name=(forum.name if forum else None),
                                       old_forum_slug=(forum.slug if forum else None),
                                       )

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

    def merge_with(self, thread):
        merge_thread.send(sender=self, new_thread=thread)

    def update_current_dates(self):
        self.post_set.update(current_date=timezone.now())

    def sync(self):
        # Counters
        self.replies = self.post_set.filter(moderated=False).count() - 1
        if self.replies < 0:
            self.replies = 0
        self.replies_reported = self.post_set.filter(reported=True).count()
        self.replies_moderated = self.post_set.filter(moderated=True).count()
        self.replies_deleted = self.post_set.filter(deleted=True).count()
        # First post
        start_post = self.post_set.order_by('id')[0:][0]
        self.start = start_post.date
        self.start_post = start_post
        self.start_poster = start_post.user
        self.start_poster_name = start_post.user_name
        self.start_poster_slug = slugify(start_post.user_name)
        self.start_poster_style = start_post.user.rank.style if start_post.user and start_post.user.rank else ''
        self.upvotes = start_post.upvotes
        self.downvotes = start_post.downvotes
        # Last visible post
        if self.replies > 0:
            last_post = self.post_set.order_by('-id').filter(moderated=False)[0:][0]
        else:
            last_post = start_post
        self.last = last_post.date
        self.last_post = last_post
        self.last_poster = last_post.user
        self.last_poster_name = last_post.user_name
        self.last_poster_slug = slugify(last_post.user_name)
        self.last_poster_style = last_post.user.rank.style if last_post.user and last_post.user.rank else ''
        # Flags
        self.moderated = start_post.moderated
        self.deleted = start_post.deleted

    def email_watchers(self, request, thread_type, post):
        from misago.acl.builder import acl
        from misago.acl.exceptions import ACLError403, ACLError404
        from misago.models import ThreadRead, WatchedThread

        notified = []
        for watch in WatchedThread.objects.filter(thread=self).filter(last_read__gte=self.previous_last.date):
            user = watch.user
            if user.pk != request.user.pk:
                try:
                    user_acl = acl(request, user)
                    user_acl.forums.allow_forum_view(self.forum)
                    user_acl.threads.allow_thread_view(user, self)
                    user_acl.threads.allow_post_view(user, self, post)
                    if not user.is_ignoring(request.user):
                        if watch.email:
                            user.email_user(
                                            request,
                                            '%s_reply_notification' % thread_type,
                                            _('New reply in thread "%(thread)s"') % {'thread': self.name},
                                            {'author': request.user, 'post': post, 'thread': self}
                                            )
                        notified.append(user)
                except (ACLError403, ACLError404):
                    pass
        return notified


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


def report_update_handler(sender, **kwargs):
    if sender == Thread:
        thread = kwargs.get('instance')
        if thread.weight < 2 and thread.report_for_id:
            reported_post = thread.report_for
            if reported_post.reported:
                reported_post.reported = False
                reported_post.reports = None
                reported_post.save(force_update=True)
                reported_post.thread.replies_reported -= 1
                reported_post.thread.save(force_update=True)

pre_save.connect(report_update_handler, dispatch_uid="sync_post_reports_on_update")


def report_delete_handler(sender, **kwargs):
    if sender == Thread:
        thread = kwargs.get('instance')
        if thread.report_for_id:
            reported_post = thread.report_for
            if reported_post.reported:
                reported_post.reported = False
                reported_post.reports = None
                reported_post.save(force_update=True)
                reported_post.thread.replies_reported -= 1
                reported_post.thread.save(force_update=True)

pre_delete.connect(report_delete_handler, dispatch_uid="sync_post_reports_on_delete")


def delete_user_content_handler(sender, **kwargs):
    for thread in Thread.objects.filter(start_poster=sender):
        thread.delete()

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_threads")


def move_forum_content_handler(sender, **kwargs):
    Thread.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads")


def delete_user_handler(sender, instance, using, **kwargs):
    from misago.models import User
    if sender == User:
        for thread in instance.private_thread_set.all():
            thread.participants.remove(instance)
            if not thread.participants.count():
                thread.delete()

pre_delete.connect(delete_user_handler, dispatch_uid="delete_user_participations")


def sync_user_handler(sender, **kwargs):
    sender.threads = sender.thread_set.count()

sync_user_profile.connect(sync_user_handler, dispatch_uid="sync_user_threads")
