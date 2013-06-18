from django.db import models
from django.db.models import F
from django.db.models.signals import pre_save, pre_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.markdown import clear_markdown
from misago.signals import (delete_user_content, merge_post, merge_thread,
                            move_forum_content, move_post, move_thread,
                            rename_user, sync_user_profile)
from misago.utils.translation import ugettext_lazy

class PostManager(models.Manager):
    def filter_stats(self, start, end):
        return self.filter(date__gte=start).filter(date__lte=end)


class Post(models.Model):
    forum = models.ForeignKey('Forum')
    thread = models.ForeignKey('Thread')
    merge = models.PositiveIntegerField(default=0)
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    user_name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    post = models.TextField()
    post_preparsed = models.TextField()
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    mentions = models.ManyToManyField('User', related_name="mention_set")
    checkpoints = models.BooleanField(default=False)
    date = models.DateTimeField()
    edits = models.PositiveIntegerField(default=0)
    edit_date = models.DateTimeField(null=True, blank=True)
    edit_reason = models.CharField(max_length=255, null=True, blank=True)
    edit_user = models.ForeignKey('User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    edit_user_name = models.CharField(max_length=255, null=True, blank=True)
    edit_user_slug = models.SlugField(max_length=255, null=True, blank=True)
    reported = models.BooleanField(default=False, db_index=True)
    moderated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)

    objects = PostManager()

    statistics_name = _('New Posts')

    class Meta:
        app_label = 'misago'

    def delete(self, *args, **kwargs):
        """
        FUGLY HAX for weird stuff that happens with
        relations on model deletion in MySQL
        """
        if self.reported:
            self.report_set.update(report_for=None)
        return super(Post, self).delete(*args, **kwargs)

    def get_date(self):
        return self.date

    def quote(self):
        quote = []
        quote.append('@%s' % self.user_name)
        for line in self.post.splitlines():
            quote.append('> %s' % line)
        quote.append('\r\n')
        return '\r\n'.join(quote)

    @property
    def post_clean(self):
        return clear_markdown(self.post_preparsed)

    def move_to(self, thread):
        move_post.send(sender=self, move_to=thread)
        self.thread = thread
        self.forum = thread.forum
        
    def merge_with(self, post):
        post.post = '%s\n- - -\n%s' % (post.post, self.post)
        merge_post.send(sender=self, new_post=post)

    def set_checkpoint(self, request, action, user=None, forum=None):
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
                                       target_user=user,
                                       target_user_name=(user.username if user else None),
                                       target_user_slug=(user.username_slug if user else None),
                                       old_forum=forum,
                                       old_forum_name=(forum.name if forum else None),
                                       old_forum_slug=(forum.slug if forum else None),
                                       )
            
    def notify_mentioned(self, request, thread_type, users):
        from misago.acl.builder import acl
        from misago.acl.exceptions import ACLError403, ACLError404
        
        mentioned = self.mentions.all()
        for slug, user in users.items():
            if user.pk != request.user.pk and user not in mentioned:
                self.mentions.add(user)
                try:                    
                    acl = acl(request, user)
                    acl.forums.allow_forum_view(self.forum)
                    acl.threads.allow_thread_view(user, self.thread)
                    acl.threads.allow_post_view(user, self.thread, self)
                    if not user.is_ignoring(request.user):
                        alert = user.alert(ugettext_lazy("%(username)s has mentioned you in his reply in thread %(thread)s").message)
                        alert.profile('username', request.user)
                        alert.post('thread', thread_type, self.thread, self)
                        alert.save_all()
                except (ACLError403, ACLError404):
                    pass

    def is_reported(self):
        self.reported = self.report_set.filter(weight=2).count() > 0

    def live_report(self):
        try:
            return self.report_set.filter(weight=2)[0]
        except IndexError:
            return None


def rename_user_handler(sender, **kwargs):
    Post.objects.filter(user=sender).update(
                                            user_name=sender.username,
                                            )
    Post.objects.filter(edit_user=sender).update(
                                                 edit_user_name=sender.username,
                                                 edit_user_slug=sender.username_slug,
                                                 )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_posts")


def delete_user_content_handler(sender, **kwargs):
    from misago.models import Thread

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

    for post in Post.objects.filter(user=sender):
        post.delete()

    for thread in Thread.objects.filter(id__in=threads):
        thread.sync()
        thread.save(force_update=True)

delete_user_content.connect(delete_user_content_handler, dispatch_uid="delete_user_posts")


def move_forum_content_handler(sender, **kwargs):
    Post.objects.filter(forum=sender).update(forum=kwargs['move_to'])

move_forum_content.connect(move_forum_content_handler, dispatch_uid="move_forum_posts")


def move_thread_handler(sender, **kwargs):
    Post.objects.filter(thread=sender).update(forum=kwargs['move_to'])

move_thread.connect(move_thread_handler, dispatch_uid="move_thread_posts")


def merge_thread_handler(sender, **kwargs):
    Post.objects.filter(thread=sender).update(thread=kwargs['new_thread'], merge=F('merge') + kwargs['merge'])

merge_thread.connect(merge_thread_handler, dispatch_uid="merge_threads_posts")


def sync_user_handler(sender, **kwargs):
    sender.posts = sender.post_set.count()

sync_user_profile.connect(sync_user_handler, dispatch_uid="sync_user_posts")
