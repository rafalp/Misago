from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from misago.acl import version as acl_version
from misago.acl.models import BaseRole
from misago.core import serializer
from misago.core.cache import cache
from misago.core.signals import secret_key_changed
from misago.core.utils import slugify


CACHE_NAME = 'misago_forums_tree'
FORUMS_TREE_ID = 1


class ForumManager(TreeManager):
    def private_threads(self):
        return self.get(special_role='private_threads')

    def root_category(self):
        return self.get(special_role='root_category')

    def all_forums(self, include_root=False):
        qs = self.filter(tree_id=FORUMS_TREE_ID)
        if not include_root:
            qs = self.filter(lft__gt=3)
        return qs.order_by('lft')

    def get_cached_forums_dict(self):
        forums_dict = cache.get(CACHE_NAME, 'nada')
        if forums_dict == 'nada':
            forums_dict = self.get_forums_dict_from_db()
            cache.set(CACHE_NAME, forums_dict)
        return forums_dict

    def get_forums_dict_from_db(self):
        forums_dict = {}
        for forum in self.all_forums(include_root=True):
            forums_dict[forum.pk] = forum
        return forums_dict

    def clear_cache(self):
        cache.delete(CACHE_NAME)


class Forum(MPTTModel):
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    special_role = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    redirect_url = models.CharField(max_length=255, null=True, blank=True)
    redirects = models.PositiveIntegerField(default=0)
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    prune_started_after = models.PositiveIntegerField(default=0)
    prune_replied_after = models.PositiveIntegerField(default=0)
    archive_pruned_in = models.ForeignKey('self',
                                          related_name='pruned_archive',
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)
    css_class = models.CharField(max_length=255, null=True, blank=True)

    objects = ForumManager()

    def __unicode__(self):
        if self.special_role == 'root_category':
            return unicode(_('None (will become top level category)'))
        elif self.special_role == 'private_threads':
            return unicode(_('Private Threads'))
        else:
            return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            acl_version.invalidate()
        return super(Forum, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Forum.objects.clear_cache()
        acl_version.invalidate()
        return super(Forum, self).delete(*args, **kwargs)

    @property
    def redirect_host(self):
        return urlparse(self.redirect_url).hostname

    def get_absolute_url(self):
        if not self.special_role:
            if self.level == 1:
                formats = (reverse('misago:index'), self.slug, self.pk)
                return '%s#%s-%s' % formats
            else:
                return reverse('misago:%s' % self.role, kwargs={
                    'forum_id': self.pk, 'forum_slug': self.slug
                })
        else:
            return None

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def has_child(self, child):
        return child.lft > self.lft and child.rght < self.rght


class ForumRole(BaseRole):
    pass


class RoleForumACL(models.Model):
    role = models.ForeignKey('misago_acl.Role', related_name='forums_acls')
    forum = models.ForeignKey('Forum', related_name='forum_role_set')
    forum_role = models.ForeignKey(ForumRole)


"""
Signal handlers
"""
@receiver(secret_key_changed)
def update_roles_pickles(sender, **kwargs):
    for role in ForumRole.objects.iterator():
        if role.pickled_permissions:
            role.pickled_permissions = serializer.regenerate_checksum(
                role.pickled_permissions)
            role.save(update_fields=['pickled_permissions'])
