from django.db import models
from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey


class ForumManager(TreeManager):
    pass


class Forum(MPTTModel):
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children')
    special_role = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank=True)
    description_preparsed = models.TextField(null=True, blank=True)
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
