from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from misago.acl import version as acl_version
from misago.acl.models import BaseRole
from misago.core import serializer
from misago.core.signals import secret_key_changed
from misago.core.utils import subset_markdown, slugify


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


class Forum(MPTTModel):
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    special_role = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_as_html = models.TextField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    redirect_url = models.CharField(max_length=255, null=True, blank=True)
    redirects_count = models.PositiveIntegerField(default=0)
    threads = models.PositiveIntegerField(default=0)
    threads_count = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
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
        acl_version.invalidate()
        return super(Forum, self).delete(*args, **kwargs)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_description(self, description):
        self.description = description
        self.description_as_html = subset_markdown(description)

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
