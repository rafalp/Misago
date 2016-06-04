from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from misago.acl import version as acl_version
from misago.acl.models import BaseRole
from misago.conf import settings
from misago.core.cache import cache
from misago.core.utils import slugify
from misago.threads import threadtypes


CACHE_NAME = 'misago_categories_tree'
CATEGORIES_TREE_ID = 1


class CategoryManager(TreeManager):
    def private_threads(self):
        return self.get_special('private_threads')

    def root_category(self):
        return self.get_special('root_category')

    def get_special(self, special_role):
        cache_name = '%s_%s' % (CACHE_NAME, special_role)

        special_category = cache.get(cache_name, 'nada')
        if special_category == 'nada':
            special_category = self.get(special_role=special_role)
            cache.set(cache_name, special_category)
        return special_category

    def all_categories(self, include_root=False):
        qs = self.filter(tree_id=CATEGORIES_TREE_ID)
        if not include_root:
            qs = qs.filter(level__gt=0)
        return qs.order_by('lft')

    def get_cached_categories_dict(self):
        categories_dict = cache.get(CACHE_NAME, 'nada')
        if categories_dict == 'nada':
            categories_dict = self.get_categories_dict_from_db()
            cache.set(CACHE_NAME, categories_dict)
        return categories_dict

    def get_categories_dict_from_db(self):
        categories_dict = {}
        for category in self.all_categories(include_root=True):
            categories_dict[category.pk] = category
        return categories_dict

    def clear_cache(self):
        cache.delete(CACHE_NAME)


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children'
    )
    special_role = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    last_post_on = models.DateTimeField(null=True, blank=True)
    last_thread = models.ForeignKey(
        'misago_threads.Thread',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    last_thread_title = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.CharField(max_length=255, null=True, blank=True)
    last_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.CharField(max_length=255, null=True, blank=True)
    prune_started_after = models.PositiveIntegerField(default=0)
    prune_replied_after = models.PositiveIntegerField(default=0)
    archive_pruned_in = models.ForeignKey(
        'self',
        related_name='pruned_archive',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    css_class = models.CharField(max_length=255, null=True, blank=True)

    objects = CategoryManager()

    @property
    def thread_type(self):
        return threadtypes.get(self.special_role or 'category')

    def __unicode__(self):
        return unicode(self.thread_type.get_category_name(self))

    def lock(self):
        return Category.objects.select_for_update().get(id=self.id)

    def delete(self, *args, **kwargs):
        Category.objects.clear_cache()
        acl_version.invalidate()
        return super(Category, self).delete(*args, **kwargs)

    def synchronize(self):
        self.threads = self.thread_set.filter(is_unapproved=False).count()

        if self.threads:
            replies_sum = self.thread_set.aggregate(models.Sum('replies'))
            self.posts = self.threads + replies_sum['replies__sum']
        else:
            self.posts = 0

        if self.threads:
            last_thread_qs = self.thread_set.filter(is_unapproved=False)
            last_thread = last_thread_qs.order_by('-last_post_on')[:1][0]
            self.set_last_thread(last_thread)
        else:
            self.empty_last_thread()

    def delete_content(self):
        from misago.categories.signals import delete_category_content
        delete_category_content.send(sender=self)

    def move_content(self, new_category):
        from misago.categories.signals import move_category_content
        move_category_content.send(sender=self, new_category=new_category)

    def get_absolute_url(self):
        return self.thread_type.get_category_absolute_url(self)

    def get_last_thread_url(self):
        return self.thread_type.get_category_last_thread_url(self)

    def get_last_post_url(self):
        return self.thread_type.get_category_last_post_url(self)

    def get_api_read_url(self):
        return self.thread_type.get_category_api_read_url(self)

    def set_name(self, name):
        self.name = name
        self.slug = slugify(name)

    def set_last_thread(self, thread):
        self.last_post_on = thread.last_post_on
        self.last_thread = thread
        self.last_thread_title = thread.title
        self.last_thread_slug = thread.slug
        self.last_poster = thread.last_poster
        self.last_poster_name = thread.last_poster_name
        self.last_poster_slug = thread.last_poster_slug

    def empty_last_thread(self):
        self.last_post_on = None
        self.last_thread = None
        self.last_thread_title = None
        self.last_thread_slug = None
        self.last_poster = None
        self.last_poster_name = None
        self.last_poster_slug = None

    def has_child(self, child):
        return child.lft > self.lft and child.rght < self.rght


class CategoryRole(BaseRole):
    pass


class RoleCategoryACL(models.Model):
    role = models.ForeignKey('misago_acl.Role', related_name='categories_acls')
    category = models.ForeignKey('Category', related_name='category_role_set')
    category_role = models.ForeignKey(CategoryRole)
