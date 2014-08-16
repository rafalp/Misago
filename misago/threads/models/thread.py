from django.db import models

from misago.conf import settings


class Thread(object):#(models.Model):
    forum = models.ForeignKey('Forum')
    weight = models.PositiveIntegerField(default=0)
    prefix = models.ForeignKey('ThreadPrefix', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    has_reported_posts = models.BooleanField(default=False)
    has_moderated_posts = models.BooleanField(default=False)
    has_deleted_posts = models.BooleanField(default=False)
    start = models.DateTimeField()
    start_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    start_poster = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)
    start_poster_name = models.CharField(max_length=255)
    start_poster_slug = models.SlugField(max_length=255)
    last = models.DateTimeField()
    last_post = models.ForeignKey('Post', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster = models.ForeignKey('User', related_name='+', null=True, blank=True, on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    is_poll = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
