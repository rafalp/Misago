from django.db import models

from misago.conf import settings
from misago.core.utils import slugify


__all__ = ['ANNOUNCEMENT', 'PINNED', 'Thread']


ANNOUNCEMENT = 2
PINNED = 1


class Thread(models.Model):
    forum = models.ForeignKey('misago_forums.Forum')
    weight = models.PositiveIntegerField(default=0)
    prefix = models.ForeignKey('misago_threads.Prefix',
                               null=True, blank=True,
                               on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
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

    def is_announcement(self):
        return self.weight == ANNOUNCEMENT

    def is_pinned(self):
        return self.weight == PINNED

    def get_absolute_url(self):
        pass

    def get_new_reply_url(self):
        pass

    def get_last_reply_url(self):
        pass

    def set_title(self, title):
        self.title = title
        self.slug = slugify(title)

    def set_first_post(self, post):
        self.started_on = post.posted_on
        self.first_post = post
        self.starter = post.poster
        self.starter_name = post.poster_name
        if post.poster:
            self.starter_slug = post.poster.slug
        else:
            self.starter_slug = slugify(post.poster_name)

    def set_last_post(self, post):
        self.last_post_on = post.posted_on
        self.last_post = post
        self.last_poster = post.poster
        self.last_poster_name = post.poster_name
        if post.poster:
            self.last_poster_slug = post.poster.slug
        else:
            self.last_poster_slug = slugify(post.poster_name)
