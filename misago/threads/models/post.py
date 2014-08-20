from django.db import models

from misago.conf import settings

from misago.threads.checksums import is_post_valid


class Post(models.Model):
    forum = models.ForeignKey('misago_forums.Forum')
    thread = models.ForeignKey('misago_threads.Thread')
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               on_delete=models.SET_NULL)
    poster_name = models.CharField(max_length=255)
    poster_ip = models.GenericIPAddressField()
    original = models.TextField()
    parsed = models.TextField()
    checksum = models.CharField(max_length=64)
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
    is_reported = models.BooleanField(default=False, db_index=True)
    is_moderated = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_protected = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return is_post_valid(self)
