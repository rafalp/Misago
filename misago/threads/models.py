from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.forums.signals import move_forum_content
from misago.threads.signals import move_thread, merge_thread, move_post, merge_post
from misago.users.signals import delete_user_content, rename_user
from misago.utils import slugify, ugettext_lazy
from misago.watcher.models import ThreadWatch

class ThreadManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(start__gte=start).filter(start__lte=end)


class Thread(models.Model):
    forum = models.ForeignKey('forums.Forum')
    weight = models.PositiveIntegerField(default=0, db_index=True)
    type = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    replies_reported = models.PositiveIntegerField(default=0)
    replies_moderated = models.PositiveIntegerField(default=0)
    replies_deleted = models.PositiveIntegerField(default=0)
    merges = models.PositiveIntegerField(default=0, db_index=True)
    score = models.PositiveIntegerField(default=30, db_index=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    start = models.DateTimeField(db_index=True)
    start_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    start_poster = models.ForeignKey('users.User', null=True, blank=True)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    start_poster_style = models.CharField(max_length=255, null=True, blank=True)
    last = models.DateTimeField(db_index=True)
    last_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster = models.ForeignKey('users.User', related_name='+', null=True, blank=True)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    moderated = models.BooleanField(default=False, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    closed = models.BooleanField(default=False)

    objects = ThreadManager()

    statistics_name = _('New Threads')

    def get_date(self):
        return self.start

    def move_to(self, move_to):
        move_thread.send(sender=self, move_to=move_to)
        self.forum = move_to

    def merge_with(self, thread, merge):
        merge_thread.send(sender=self, new_thread=thread, merge=merge)

    def sync(self):
        # Counters
        self.replies = self.post_set.filter(moderated=False).filter(deleted=False).count() - 1
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
        # Last post
        if self.replies > 0:
            last_post = self.post_set.order_by('-merge', '-id').filter(moderated=False).filter(deleted=False)[0:][0]
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
        from misago.acl.builder import get_acl
        from misago.acl.utils import ACLError403, ACLError404
        
        for watch in ThreadWatch.objects.filter(thread=self).filter(email=True).filter(last_read__gte=self.previous_last):
            user = watch.user
            if user.pk != request.user.pk:
                try:
                    acl = get_acl(request, user)
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


class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)


class Post(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    merge = models.PositiveIntegerField(default=0, db_index=True)
    user = models.ForeignKey('users.User', null=True, blank=True)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    mentions = models.ManyToManyField('users.User', related_name="mention_set")
    checkpoints = models.BooleanField(default=False, db_index=True)
    date = models.DateTimeField()
    edits = models.PositiveIntegerField(default=0)
    edit_date = models.DateTimeField(null=True, blank=True)
    edit_reason = models.CharField(max_length=255, null=True, blank=True)
    edit_user = models.ForeignKey('users.User', related_name='+', null=True)
    edit_user_name = models.CharField(max_length=255, null=True, blank=True)
    edit_user_slug = models.SlugField(max_length=255, null=True, blank=True)
    reported = models.BooleanField(default=False)
    moderated = models.BooleanField(default=False, db_index=True)
    deleted = models.BooleanField(default=False, db_index=True)
    protected = models.BooleanField(default=False)

    objects = PostManager()

    statistics_name = _('New Posts')

    def get_date(self):
        return self.date

    def move_to(self, thread):
        move_post.send(sender=self, move_to=thread)
        self.thread = thread
        self.forum = thread.forum
        
    def merge_with(self, post):
        post.post = '%s\n- - -\n%s' % (post.post, self.post)
        merge_post.send(sender=self, new_post=post)

    def set_checkpoint(self, request, action):
        if request.user.is_authenticated():
            self.checkpoints = True
            self.checkpoint_set.create(
                                       forum=self.forum,
                                       thread=self.thread,
                                       post=self,
                                       action=action,
                                       user=request.user,
                                       user_name=request.user.username,
                                       user_slug=request.user.username_slug,
                                       date=timezone.now(),
                                       ip=request.session.get_ip(request),
                                       agent=request.META.get('HTTP_USER_AGENT'),
                                       )
            
    def notify_mentioned(self, request, users):
        from misago.acl.builder import get_acl
        from misago.acl.utils import ACLError403, ACLError404
        
        mentioned = self.mentions.all()
        for slug, user in users.items():
            if user.pk != request.user.pk and user not in mentioned:
                self.mentions.add(user)
                try:                    
                    acl = get_acl(request, user)
                    acl.forums.allow_forum_view(self.forum)
                    acl.threads.allow_thread_view(user, self.thread)
                    acl.threads.allow_post_view(user, self.thread, self)
                    if not user.is_ignoring(request.user):
                        alert = user.alert(ugettext_lazy("%(username)s has mentioned you in his reply in thread %(thread)s").message)
                        alert.profile('username', request.user)
                        alert.post('thread', self.thread, self)
                        alert.save_all()
                except (ACLError403, ACLError404):
                    pass


class Change(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post)
    user = models.ForeignKey('users.User', null=True, blank=True)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    reason = models.CharField(max_length=255, null=True, blank=True)
    thread_name_new = models.CharField(max_length=255, null=True, blank=True)
    thread_name_old = models.CharField(max_length=255, null=True, blank=True)
    post_content = models.TextField()
    size = models.IntegerField(default=0)
    change = models.IntegerField(default=0)


class Checkpoint(models.Model):
    forum = models.ForeignKey('forums.Forum')
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post)
    action = models.CharField(max_length=255)
    user = models.ForeignKey('users.User', null=True, blank=True)
    user_name = models.CharField(max_length=255)
    user_slug = models.CharField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)


"""
Signals
"""
def rename_user_handler(sender, **kwargs):
    Thread.objects.filter(start_poster=sender).update(
                                                     start_poster_name=sender.username,
                                                     start_poster_slug=sender.username_slug,
                                                     )
    Thread.objects.filter(last_poster=sender).update(
                                                     last_poster_name=sender.username,
                                                     last_poster_slug=sender.username_slug,
                                                     )
    Post.objects.filter(user=sender).update(
                                            user_name=sender.username,
                                            )
    Post.objects.filter(edit_user=sender).update(
                                                 edit_user_name=sender.username,
                                                 edit_user_slug=sender.username_slug,
                                                 )
    Change.objects.filter(user=sender).update(
                                              user_name=sender.username,
                                              user_slug=sender.username_slug,
                                              )
    Checkpoint.objects.filter(user=sender).update(
                                                  user_name=sender.username,
                                                  user_slug=sender.username_slug,
                                                  )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_threads")


def delete_user_content_handler(sender, **kwargs):
    Thread.objects.filter(start_poster=sender).delete()
    threads = []
    prev_posts = []
    for post in sender.post_set.filter(checkpoints=True):
        threads.append(post.thread_id)
        prev_post = Post.objects.filter(thread=post.thread_id).exclude(merge__gt=post.merge).exclude(user=sender).order_by('merge', '-id')[:1][0]
        post.checkpoint_set.update(post=prev_post)
        if not prev_post.pk in prev_posts:
            prev_posts.append(prev_post.pk)
    sender.post_set.all().delete()
    Post.objects.filter(id__in=prev_posts).update(checkpoints=True)
    for post in sender.post_set.distinct().values('thread_id').iterator():
        if not post['thread_id'] in threads:
            threads.append(post['thread_id'])
    Post.objects.filter(user=sender).delete()
    for thread in Thread.objects.filter(id__in=threads):
        thread.sync()
        thread.save(force_update=True)

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_threads_posts")


def move_forum_content_handler(sender, **kwargs):
    Thread.objects.filter(forum=sender).update(forum=kwargs['move_to'])
    Post.objects.filter(forum=sender).update(forum=kwargs['move_to'])
    Change.objects.filter(forum=sender).update(forum=kwargs['move_to'])
    Checkpoint.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_threads_posts")


def move_thread_handler(sender, **kwargs):
    Post.objects.filter(forum=sender.forum_pk).update(forum=kwargs['move_to'])
    Change.objects.filter(forum=sender.forum_pk).update(forum=kwargs['move_to'])
    Checkpoint.objects.filter(forum=sender.forum_pk).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread")


def merge_thread_handler(sender, **kwargs):
    Post.objects.filter(thread=sender).update(thread=kwargs['new_thread'], merge=F('merge') + kwargs['merge'])
    Change.objects.filter(thread=sender).update(thread=kwargs['new_thread'])
    Checkpoint.objects.filter(thread=sender).delete()

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads")


def move_posts_handler(sender, **kwargs):
    Change.objects.filter(post=sender).update(forum=kwargs['move_to'].forum, thread=kwargs['move_to'])
    if sender.checkpoints:
        prev_post = Post.objects.filter(thread=sender.thread_id).filter(merge__lte=sender.merge).exclude(id=sender.pk).order_by('merge', '-id')[:1][0]
        Checkpoint.objects.filter(post=sender).update(post=prev_post)
        prev_post.checkpoints = True
        prev_post.save(force_update=True)
    sender.checkpoints = False

move_post.connect(move_posts_handler, dispatch_uid="move_posts")


def merge_posts_handler(sender, **kwargs):
    Change.objects.filter(post=sender).update(post=kwargs['new_post'])
    Checkpoint.objects.filter(post=sender).update(post=kwargs['new_post'])
    if sender.checkpoints:
        kwargs['new_post'].checkpoints = True

merge_post.connect(merge_posts_handler, dispatch_uid="merge_posts")
