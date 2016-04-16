from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from misago.conf import settings

from misago.threads import threadtypes
from misago.threads.checksums import update_post_checksum, is_post_valid


class Post(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    thread = models.ForeignKey('misago_threads.Thread')
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               on_delete=models.SET_NULL)
    poster_name = models.CharField(max_length=255)
    poster_ip = models.GenericIPAddressField()
    original = models.TextField()
    parsed = models.TextField()
    checksum = models.CharField(max_length=64, default='-')
    mentions = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name="mention_set")

    has_attachments = models.BooleanField(default=False)
    pickled_attachments = models.TextField(null=True, blank=True)

    posted_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    edits = models.PositiveIntegerField(default=0)
    last_editor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    last_editor_name = models.CharField(max_length=255, null=True, blank=True)
    last_editor_slug = models.SlugField(max_length=255, null=True, blank=True)

    hidden_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    hidden_by_name = models.CharField(max_length=255, null=True, blank=True)
    hidden_by_slug = models.SlugField(max_length=255, null=True, blank=True)
    hidden_on = models.DateTimeField(default=timezone.now)

    has_reports = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)
    is_unapproved = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s...' % self.original[10:].strip()

    def delete(self, *args, **kwargs):
        from misago.threads.signals import delete_post
        delete_post.send(sender=self)

        super(Post, self).delete(*args, **kwargs)

    def merge(self, other_post):
        if self.thread_id != other_post.thread_id:
            message = "only posts belonging to same thread can be merged"
            raise ValueError(message)

        message = "posts made by different authors can't be merged"
        if self.poster_id and other_post.poster_id:
            if self.poster_id != other_post.poster_id:
                raise ValueError(message)
        else:
            raise ValueError(message)

        if self.pk == other_post.pk:
            raise ValueError("post can't be merged with itself")

        other_post.original = '%s\n\n%s' % (other_post.original, self.original)
        other_post.parsed = '%s\n%s' % (other_post.parsed, self.parsed)
        update_post_checksum(other_post)

        from misago.threads.signals import merge_post
        merge_post.send(sender=self, other_thread=other_post)

    def move(self, new_thread):
        from misago.threads.signals import move_post

        self.category = new_thread.category
        self.thread = new_thread
        move_post.send(sender=self)

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_absolute_url(self):
        return self.thread_type.get_post_absolute_url(self)

    def get_quote_url(self):
        return self.thread_type.get_post_quote_url(self)

    def get_approve_url(self):
        return self.thread_type.get_post_approve_url(self)

    def get_unhide_url(self):
        return self.thread_type.get_post_unhide_url(self)

    def get_hide_url(self):
        return self.thread_type.get_post_hide_url(self)

    def get_delete_url(self):
        return self.thread_type.get_post_delete_url(self)

    def get_report_url(self):
        return self.thread_type.get_post_report_url(self)

    @property
    def short(self):
        if self.is_valid:
            if len(self.original) > 150:
                return '%s...' % self.original[:150].strip()
            else:
                return self.original
        else:
            return ''

    @property
    def is_valid(self):
        return is_post_valid(self)
