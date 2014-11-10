from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver

from misago.conf import settings
from misago.core.shortcuts import paginate
from misago.core.utils import slugify


__all__ = ['Thread']


class Thread(models.Model):
    forum = models.ForeignKey('misago_forums.Forum')
    label = models.ForeignKey('misago_threads.Label',
                              null=True, blank=True,
                              on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    replies = models.PositiveIntegerField(default=0, db_index=True)
    has_reported_posts = models.BooleanField(default=False)
    has_moderated_posts = models.BooleanField(default=False)
    has_hidden_posts = models.BooleanField(default=False)
    has_events = models.BooleanField(default=False)
    started_on = models.DateTimeField(db_index=True)
    first_post = models.ForeignKey('misago_threads.Post', related_name='+',
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)
    starter = models.ForeignKey(settings.AUTH_USER_MODEL,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    starter_name = models.CharField(max_length=255)
    starter_slug = models.CharField(max_length=255)
    last_post_on = models.DateTimeField(db_index=True)
    last_post = models.ForeignKey('misago_threads.Post', related_name='+',
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    last_poster = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='last_poster_set',
                                    null=True, blank=True,
                                    on_delete=models.SET_NULL)
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.CharField(max_length=255, null=True, blank=True)
    is_pinned = models.BooleanField(default=False, db_index=True)
    is_poll = models.BooleanField(default=False)
    is_moderated = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    class Meta:
        index_together = [
            ['forum', 'id'],
            ['forum', 'last_post_on'],
            ['forum', 'replies'],
        ]

    def __unicode__(self):
        return self.title

    def lock(self):
        return Thread.objects.select_for_update().get(id=self.id)

    def delete(self, *args, **kwargs):
        from misago.threads.signals import delete_thread
        delete_thread.send(sender=self)

        super(Thread, self).delete(*args, **kwargs)

    def merge(self, other_thread):
        if self.pk == other_thread.pk:
            raise ValueError("thread can't be merged with itself")

        from misago.threads.signals import merge_thread
        merge_thread.send(sender=self, other_thread=other_thread)

    def move(self, new_forum):
        from misago.threads.signals import move_thread

        self.forum = new_forum
        move_thread.send(sender=self)

    def synchronize(self):
        self.replies = self.post_set.filter(is_moderated=False).count()
        if self.replies > 0:
            self.replies -= 1

        reported_post_qs = self.post_set.filter(is_reported=True)
        self.has_reported_posts = reported_post_qs.exists()

        moderated_post_qs = self.post_set.filter(is_moderated=True)
        self.has_moderated_posts = moderated_post_qs.exists()

        hidden_post_qs = self.post_set.filter(is_hidden=True)[:1]
        self.has_hidden_posts = hidden_post_qs.exists()

        self.has_events = self.event_set.exists()

        first_post = self.post_set.order_by('id')[:1][0]
        self.set_first_post(first_post)

        self.is_moderated = first_post.is_moderated
        self.is_hidden = first_post.is_hidden

        last_post_qs = self.post_set.filter(is_moderated=False).order_by('-id')
        last_post = last_post_qs[:1]
        if last_post:
            self.set_last_post(last_post[0])
        else:
            self.set_last_post(first_post)

    @property
    def link_prefix(self):
        if self.forum.special_role == 'private_threads':
            return 'private_thread'
        else:
            return 'thread'

    def get_url_name(self, suffix=None):
        link = 'misago:%s' % self.link_prefix
        if suffix:
            link = '%s_%s' % (link, suffix)
        return link

    def get_url(self, suffix=None):
        return reverse(self.get_url_name(suffix), kwargs={
            'thread_slug': self.slug,
            'thread_id': self.id
        })

    def get_absolute_url(self):
        return self.get_url()

    def get_last_reply_url(self):
        return self.get_url('last')

    def get_new_reply_url(self):
        return self.get_url('new')

    def get_moderated_url(self):
        return self.get_url('moderated')

    def get_reported_url(self):
        return self.get_url('reported')

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

        self.is_moderated = post.is_moderated
        self.is_hidden = post.is_hidden

    def set_last_post(self, post):
        self.last_post_on = post.posted_on
        self.last_post = post
        self.last_poster = post.poster
        self.last_poster_name = post.poster_name
        if post.poster:
            self.last_poster_slug = post.poster.slug
        else:
            self.last_poster_slug = slugify(post.poster_name)
