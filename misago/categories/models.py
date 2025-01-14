from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from ..acl.cache import clear_acl_cache
from ..acl.models import BaseRole
from ..conf import settings
from ..core.utils import slugify
from ..plugins.models import PluginDataModel
from ..threads.threadtypes import trees_map
from .enums import CategoryTree, CategoryChildrenComponent


class CategoryManager(TreeManager):
    def private_threads(self):
        return self.get(level=0, tree_id=CategoryTree.PRIVATE_THREADS)

    def root_category(self):
        return self.get(level=0, tree_id=CategoryTree.THREADS)

    def all_categories(self, include_root=False):
        queryset = self.filter(tree_id=CategoryTree.THREADS)
        if not include_root:
            queryset = queryset.filter(level__gt=0)
        return queryset.order_by("lft")


class Category(MPTTModel, PluginDataModel):
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    special_role = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    css_class = models.CharField(max_length=255, null=True, blank=True)
    allow_polls = models.BooleanField(default=True)
    delay_browse_check = models.BooleanField(default=False)
    show_started_only = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_vanilla = models.BooleanField(default=False)
    list_children_threads = models.BooleanField(default=True)
    children_categories_component = models.CharField(
        max_length=12,
        null=False,
        blank=False,
        default=CategoryChildrenComponent.FULL,
    )
    threads = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    unapproved_threads = models.PositiveIntegerField(default=0)
    unapproved_posts = models.PositiveIntegerField(default=0)
    last_post_on = models.DateTimeField(null=True, blank=True)
    last_thread = models.ForeignKey(
        "misago_threads.Thread",
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    last_thread_title = models.CharField(max_length=255, null=True, blank=True)
    last_thread_slug = models.CharField(max_length=255, null=True, blank=True)
    last_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="+",
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
        "self",
        related_name="pruned_archive",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = CategoryManager()

    class Meta:
        indexes = PluginDataModel.Meta.indexes

    def __str__(self):
        return str(self.thread_type.get_category_name(self))

    @property
    def thread_type(self):
        return trees_map.get_type_for_tree_id(self.tree_id)

    def delete(self, *args, **kwargs):
        clear_acl_cache()
        return super().delete(*args, **kwargs)

    def synchronize(self):
        threads_queryset = self.thread_set.filter(is_hidden=False, is_unapproved=False)
        self.threads = threads_queryset.count()

        if self.threads:
            replies_sum = threads_queryset.aggregate(models.Sum("replies"))
            self.posts = self.threads + replies_sum["replies__sum"]
        else:
            self.posts = 0

        if self.threads:
            last_thread_qs = threads_queryset.filter(
                is_hidden=False, is_unapproved=False
            )
            last_thread = last_thread_qs.order_by("-last_post_on")[:1][0]
            self.set_last_thread(last_thread)
        else:
            self.empty_last_thread()

    def get_absolute_url(self):
        return self.thread_type.get_category_absolute_url(self)

    def get_last_thread_url(self):
        return self.thread_type.get_category_last_thread_url(self)

    def get_last_thread_new_url(self):
        return self.thread_type.get_category_last_thread_new_url(self)

    def get_last_post_url(self):
        return self.thread_type.get_category_last_post_url(self)

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
        "misago_acl.Role", related_name="categories_acls", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        "Category", related_name="category_role_set", on_delete=models.CASCADE
    )
    category_role = models.ForeignKey(CategoryRole, on_delete=models.CASCADE)
