from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey
from misago.admin import site
from misago.core.utils import subset_markdown, slugify


class ForumManager(TreeManager):
    def private_threads(self):
        return self.get(special_role='private_threads')

    def root_category(self):
        return self.get(special_role='root_category')

    def all_forums(self, include_root=False):
        qs = self.filter(tree_id=1)
        if not include_root:
            qs = self.filter(lft__gt=3)
        return qs


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
    archive_pruned_in = models.ForeignKey(
        'self',
        related_name='pruned_archive',
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    css_class = models.CharField(max_length=255, null=True, blank=True)

    objects = ForumManager()

    def __unicode__(self):
        if self.special_role == 'root_category':
            return unicode(_('No parent'))
        elif self.special_role == 'private_threads':
            return unicode(_('Private Threads'))
        else:
            return self.name

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_description(self, description):
        self.description = description
        self.description_as_html = subset_markdown(description)


"""register model in misago admin"""
site.add_node(
    parent='misago:admin',
    before='misago:admin:permissions:users:index',
    namespace='misago:admin:forums',
    link='misago:admin:forums:nodes:index',
    name=_("Forums"),
    icon='fa fa-comment')

site.add_node(
    parent='misago:admin:forums',
    namespace='misago:admin:forums:nodes',
    link='misago:admin:forums:nodes:index',
    name=_("Forums Hierarchy"),
    icon='fa fa-comment')
