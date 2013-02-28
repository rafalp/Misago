from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from misago.forums.signals import move_forum_content, delete_forum_content
from misago.roles.models import Role
from misago.users.signals import rename_user

class ForumManager(models.Manager):
    forums_tree = None

    def token_to_pk(self, token):
        self.populate_tree()
        try:
            return self.forums_tree[token].pk
        except KeyError:
            return 0

    def populate_tree(self, force=False):
        if not self.forums_tree:
            self.forums_tree = cache.get('forums_tree')
        if not self.forums_tree or force:
            self.forums_tree = {}
            for forum in Forum.objects.order_by('lft'):
                self.forums_tree[forum.pk] = forum
                if forum.token:
                    self.forums_tree[forum.token] = forum
            cache.set('forums_tree', self.forums_tree)

    def forum_parents(self, forum, include_self=False):
        self.populate_tree()
        parents = []
        parent = self.forums_tree[forum]
        if include_self:
            parents.append(parent)
        while parent.level > 1:
            parent = self.forums_tree[parent.parent_id]
            parents.append(parent)
        result = []
        for i in reversed(parents):
            result.append(i)
        return list(result)

    def parents_aware_forum(self, forum):
        self.populate_tree()
        proxy = Forum()
        try:
            proxy.id = forum.pk
            proxy.pk = forum.pk
        except AttributeError:
            proxy.id = forum
            proxy.pk = forum
        proxy.closed = False
        for parent in self.forum_parents(proxy.pk):
            if parent.closed:
                proxy.closed = True
                return proxy
        return proxy

    def treelist(self, acl, parent=None, tracker=None):
        complete_list = []
        forums_list = []
        parents = {}

        if parent:
            queryset = Forum.objects.filter(pk__in=acl.known_forums).filter(lft__gt=parent.lft).filter(rght__lt=parent.rght).order_by('lft')
        else:
            queryset = Forum.objects.filter(pk__in=acl.known_forums).order_by('lft')

        for forum in queryset:
            forum.subforums = []
            forum.is_read = False
            if tracker:
                forum.is_read = tracker.is_read(forum)
            parents[forum.pk] = forum
            complete_list.append(forum)
            if forum.parent_id in parents:
                parents[forum.parent_id].subforums.append(forum)
            else:
                forums_list.append(forum)

        # Second iteration - sum up forum counters
        for forum in reversed(complete_list):
            if forum.parent_id in parents and parents[forum.parent_id].type != 'redirect':
                parents[forum.parent_id].threads += forum.threads
                parents[forum.parent_id].posts += forum.posts
                if acl.can_browse(forum.pk):
                    # If forum is unread, make parent unread too
                    if not forum.is_read:
                        parents[forum.parent_id].is_read = False
                    # Sum stats
                    if forum.last_thread_date and (not parents[forum.parent_id].last_thread_date or forum.last_thread_date > parents[forum.parent_id].last_thread_date):
                        parents[forum.parent_id].last_thread_id = forum.last_thread_id
                        parents[forum.parent_id].last_thread_name = forum.last_thread_name
                        parents[forum.parent_id].last_thread_slug = forum.last_thread_slug
                        parents[forum.parent_id].last_thread_date = forum.last_thread_date
                        parents[forum.parent_id].last_poster_id = forum.last_poster_id
                        parents[forum.parent_id].last_poster_name = forum.last_poster_name
                        parents[forum.parent_id].last_poster_slug = forum.last_poster_slug
                        parents[forum.parent_id].last_poster_style = forum.last_poster_style
        return forums_list
    
    def ignored_users(self, user, forums):
        check_ids = []
        for forum in forums:
            forum.last_poster_ignored = False
            if user.is_authenticated() and user.pk != forum.last_poster_id and forum.last_poster_id and not forum.last_poster_id in check_ids:
                check_ids.append(forum.last_poster_id)
        ignored_ids = []
        if check_ids and user.is_authenticated():
            for user in user.ignores.filter(id__in=check_ids).values('id'):
                ignored_ids.append(user['id'])


class Forum(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    type = models.CharField(max_length=12)
    token = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_preparsed = models.TextField(null=True, blank=True)
    threads = models.PositiveIntegerField(default=0)
    threads_delta = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    posts_delta = models.IntegerField(default=0)
    redirects = models.PositiveIntegerField(default=0)
    redirects_delta = models.IntegerField(default=0)
    last_thread = models.ForeignKey('threads.Thread', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_thread_name = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_thread_date = models.DateTimeField(null=True, blank=True)
    last_poster = models.ForeignKey('users.User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    last_poster_style = models.CharField(max_length=255, null=True, blank=True)
    prune_start = models.PositiveIntegerField(default=0)
    prune_last = models.PositiveIntegerField(default=0)
    redirect = models.CharField(max_length=255, null=True, blank=True)
    attrs = models.CharField(max_length=255, null=True, blank=True)
    show_details = models.BooleanField(default=True)
    style = models.CharField(max_length=255, null=True, blank=True)
    closed = models.BooleanField(default=False)

    objects = ForumManager()

    def __unicode__(self):
        if self.token == 'root':
           return unicode(_('Root Category'))
        return unicode(self.name)

    def set_description(self, description):
        self.description = description.strip()
        self.description_preparsed = ''
        if self.description:
            import markdown
            self.description_preparsed = markdown.markdown(description, safe_mode='escape', output_format=settings.OUTPUT_FORMAT)

    def copy_permissions(self, target):
        if target.pk != self.pk:
            for role in Role.objects.all():
                perms = role.get_permissions()
                try:
                    perms['forums'][self.pk] = perms['forums'][target.pk]
                    role.set_permissions(perms)
                    role.save(force_update=True)
                except KeyError:
                    pass

    def move_content(self, target):
        move_forum_content.send(sender=self, move_to=target)

    def attr(self, att):
        return att in self.attrs.split()

    def sync(self):
        self.threads = self.thread_set.filter(moderated=False).filter(deleted=False).count()
        self.posts = self.post_set.filter(moderated=False).filter(deleted=False).count()
        self.last_poster = None
        self.last_poster_name = None
        self.last_poster_slug = None
        self.last_poster_style = None
        self.last_thread = None
        self.last_thread_date = None
        self.last_thread_name = None
        self.last_thread_slug = None
        try:
            last_thread = self.thread_set.filter(moderated=False).filter(deleted=False).order_by('-last').all()[0:][0]
            self.last_poster_name = last_thread.last_poster_name
            self.last_poster_slug = last_thread.last_poster_slug
            self.last_poster_style = last_thread.last_poster_style
            if last_thread.last_poster:
                self.last_poster = last_thread.last_poster
            self.last_thread = last_thread
            self.last_thread_date = last_thread.start
            self.last_thread_name = last_thread.name
            self.last_thread_slug = last_thread.slug
        except (IndexError, AttributeError):
            pass

    def prune(self):
        pass
    
    def delete(self, *args, **kwargs):
        delete_forum_content.send(sender=self)
        super(Forum, self).delete(*args, **kwargs)

"""
Signals
"""
def rename_user_handler(sender, **kwargs):
    Forum.objects.filter(last_poster=sender).update(
                                                    last_poster_name=sender.username,
                                                    last_poster_slug=sender.username_slug,
                                                    )

rename_user.connect(rename_user_handler, dispatch_uid="rename_forums_last_poster")