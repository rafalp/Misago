from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils import six, timezone

from misago.conf import settings

from .. import threadtypes
from ..checksums import is_post_valid, update_post_checksum


class Post(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    poster_name = models.CharField(max_length=255)
    poster_ip = models.GenericIPAddressField()
    original = models.TextField()
    parsed = models.TextField()
    checksum = models.CharField(max_length=64, default='-')
    mentions = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="mention_set")

    has_attachments = models.BooleanField(default=False)
    attachments_cache = JSONField(null=True, blank=True)

    posted_on = models.DateTimeField()
    updated_on = models.DateTimeField()
    hidden_on = models.DateTimeField(default=timezone.now)

    edits = models.PositiveIntegerField(default=0)
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    last_editor_name = models.CharField(max_length=255, null=True, blank=True)
    last_editor_slug = models.SlugField(max_length=255, null=True, blank=True)

    hidden_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    hidden_by_name = models.CharField(max_length=255, null=True, blank=True)
    hidden_by_slug = models.SlugField(max_length=255, null=True, blank=True)

    has_reports = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)
    is_unapproved = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)

    is_event = models.BooleanField(default=False, db_index=True)
    event_type = models.CharField(max_length=255, null=True, blank=True)
    event_context = JSONField(null=True, blank=True)

    class Meta:
        index_together = [
            ('is_event', 'is_hidden'),
            ('poster', 'posted_on')
        ]

    def __unicode__(self):
        return '%s...' % self.original[10:].strip()

    def delete(self, *args, **kwargs):
        from ..signals import delete_post
        delete_post.send(sender=self)

        super(Post, self).delete(*args, **kwargs)

    def merge(self, other_post):
        if self.thread_id != other_post.thread_id:
            raise ValueError("only posts belonging to same thread can be merged")

        if self.is_event or other_post.is_event:
            raise ValueError("can't merge events")

        if self.pk == other_post.pk:
            raise ValueError("post can't be merged with itself")

        other_post.original = six.text_type('\n\n').join((other_post.original, self.original))
        other_post.parsed = six.text_type('\n').join((other_post.parsed, self.parsed))
        update_post_checksum(other_post)

        from ..signals import merge_post
        merge_post.send(sender=self, other_post=other_post)

    def move(self, new_thread):
        from ..signals import move_post

        self.category = new_thread.category
        self.thread = new_thread
        move_post.send(sender=self)

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_api_url(self):
        return self.thread_type.get_post_api_url(self)

    def get_editor_api_url(self):
        return self.thread_type.get_post_editor_api_url(self)

    def get_read_api_url(self):
        return self.thread_type.get_post_read_api_url(self)

    def get_absolute_url(self):
        return self.thread_type.get_post_absolute_url(self)

    @property
    def short(self):
        if self.is_valid:
            if len(self.original) > 150:
                return six.text_type('%s...') % self.original[:150].strip()
            else:
                return self.original
        else:
            return ''

    @property
    def is_valid(self):
        return is_post_valid(self)

    @property
    def is_first_post(self):
        return self.pk == self.thread.first_post_id
