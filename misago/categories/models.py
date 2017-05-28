from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible

from misago.acl import version as acl_version
from misago.acl.models import BaseRole
from misago.conf import settings
from misago.core.cache import cache
from misago.core.utils import slugify
from misago.threads.threadtypes import trees_map

from . import PRIVATE_THREADS_ROOT_NAME, THREADS_ROOT_NAME


CACHE_NAME = 'misago_categories_tree'


class CategoryManager(TreeManager):
    def private_threads(self):
        return self.get_special(PRIVATE_THREADS_ROOT_NAME)

    def root_category(self):
        return self.get_special(THREADS_ROOT_NAME)

    def get_special(self, special_role):
        cache_name = '%s_%s' % (CACHE_NAME, special_role)

        special_category = cache.get(cache_name, 'nada')
        if special_category == 'nada':
            special_category = self.get(special_role=special_role)
            cache.set(cache_name, special_category)
        return special_category

    def all_categories(self, include_root=False):
        tree_id = trees_map.get_tree_id_for_root(THREADS_ROOT_NAME)
        queryset = self.filter(tree_id=tree_id)
        if not include_root:
            queryset = queryset.filter(level__gt=0)
        return queryset.order_by('lft')

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


@python_2_unicode_compatible
class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE,
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
        on_delete=models.SET_NULL,
    )
    last_thread_title = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.CharField(max_length=255, null=True, blank=True)
    last_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.CharField(max_length=255, null=True, blank=True)
    require_threads_approval = models.BooleanField(default=False)
    require_replies_approval = models.BooleanField(default=False)
    require_edits_approval = models.BooleanField(default=False)
    prune_started_after = models.PositiveIntegerField(default=0)
    prune_replied_after = models.PositiveIntegerField(default=0)
    archive_pruned_in = models.ForeignKey(
        'self',
        related_name='pruned_archive',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    css_class = models.CharField(max_length=255, null=True, blank=True)

    objects = CategoryManager()

    def __str__(self):
        return six.text_type(self.thread_type.get_category_name(self))

    @property
    def thread_type(self):
        return trees_map.get_type_for_tree_id(self.tree_id)

    def delete(self, *args, **kwargs):
        Category.objects.clear_cache()
        acl_version.invalidate()
        return super(Category, self).delete(*args, **kwargs)

    def synchronize(self):
        threads_queryset = self.thread_set.filter(is_hidden=False, is_unapproved=False)
        self.threads = threads_queryset.count()

        if self.threads:
            replies_sum = threads_queryset.aggregate(models.Sum('replies'))
            self.posts = self.threads + replies_sum['replies__sum']
        else:
            self.posts = 0

        if self.threads:
            last_thread_qs = threads_queryset.filter(is_hidden=False, is_unapproved=False)
            last_thread = last_thread_qs.order_by('-last_post_on')[:1][0]
            self.set_last_thread(last_thread)
        else:
            self.empty_last_thread()

    def delete_content(self):
        from .signals import delete_category_content
        delete_category_content.send(sender=self)

    def move_content(self, new_category):
        from .signals import move_category_content
        move_category_content.send(sender=self, new_category=new_category)

    def get_absolute_url(self):
        return self.thread_type.get_category_absolute_url(self)

    def get_last_thread_url(self):
        return self.thread_type.get_category_last_thread_url(self)

    def get_last_thread_new_url(self):
        return self.thread_type.get_category_last_thread_new_url(self)

    def get_last_post_url(self):
        return self.thread_type.get_category_last_post_url(self)

    def get_read_api_url(self):
        return self.thread_type.get_category_read_api_url(self)

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
    role = models.ForeignKey(
        'misago_acl.Role',
        related_name='categories_acls',
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'Category',
        related_name='category_role_set',
        on_delete=models.CASCADE,
    )
    category_role = models.ForeignKey(CategoryRole, on_delete=models.CASCADE)
