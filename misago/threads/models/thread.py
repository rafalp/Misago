from django.db import models

from misago.conf import settings


class Thread(models.Model):
    forum = models.ForeignKey('misago_forums.Forum')
    weight = models.PositiveIntegerField(default=0)
    prefix = models.ForeignKey('misago_threads.Prefix', null=True, blank=True,
                               on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    replies = models.PositiveIntegerField(default=0)
    has_reported_posts = models.BooleanField(default=False)
    has_moderated_posts = models.BooleanField(default=False)
    has_hidden_posts = models.BooleanField(default=False)
    started_on = models.DateTimeField()
    first_post = models.ForeignKey('misago_threads.Post', related_name='+',
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    starter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    starter_name = models.CharField(max_length=255)
    starter_slug = models.SlugField(max_length=255)
    last_post_on = models.DateTimeField()
    last_post = models.ForeignKey('misago_threads.Post', related_name='+',
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    last_poster = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.SlugField(max_length=255, null=True, blank=True)
    is_poll = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
