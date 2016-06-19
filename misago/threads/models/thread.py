from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core.utils import slugify


__all__ = [
    'THREAD_WEIGHT_DEFAULT',
    'THREAD_WEIGHT_PINNED',
    'THREAD_WEIGHT_GLOBAL',
    'THREAD_WEIGHT_CHOICES',

    'Thread',
]


THREAD_WEIGHT_DEFAULT = 0
THREAD_WEIGHT_PINNED = 1
THREAD_WEIGHT_GLOBAL = 2

THREAD_WEIGHT_CHOICES = (
    (THREAD_WEIGHT_DEFAULT, _("Don't pin thread")),
    (THREAD_WEIGHT_PINNED, _("Pin thread within category")),
    (THREAD_WEIGHT_GLOBAL, _("Pin thread globally"))
)


class Thread(models.Model):
    category = models.ForeignKey('misago_categories.Category')
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    replies = models.PositiveIntegerField(default=0, db_index=True)
    has_reported_posts = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)
    has_unapproved_posts = models.BooleanField(default=False)
    has_hidden_posts = models.BooleanField(default=False)
    has_events = models.BooleanField(default=False)
    started_on = models.DateTimeField(db_index=True)

    first_post = models.ForeignKey(
        'misago_threads.Post',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    starter_name = models.CharField(max_length=255)
    starter_slug = models.CharField(max_length=255)
    last_post_on = models.DateTimeField(db_index=True)

    last_post = models.ForeignKey(
        'misago_threads.Post',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    last_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='last_poster_set',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.CharField(max_length=255, null=True, blank=True)

    weight = models.PositiveIntegerField(default=THREAD_WEIGHT_DEFAULT)

    is_poll = models.BooleanField(default=False)
    is_unapproved = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='private_thread_set',
        through='ThreadParticipant',
        through_fields=('thread', 'user')
    )

    class Meta:
        index_together = [
            ['category', 'id'],
            ['category', 'last_post_on'],
            ['category', 'replies'],
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

    def move(self, new_category):
        from misago.threads.signals import move_thread

        self.category = new_category
        move_thread.send(sender=self)

    def synchronize(self):
        self.replies = self.post_set.filter(is_unapproved=False).count()
        if self.replies > 0:
            self.replies -= 1

        reported_post_qs = self.post_set.filter(has_reports=True)
        self.has_reported_posts = reported_post_qs.exists()

        if self.has_reported_posts:
            open_reports_qs = self.post_set.filter(has_open_reports=True)
            self.has_open_reports = open_reports_qs.exists()
        else:
            self.has_open_reports = False

        unapproved_post_qs = self.post_set.filter(is_unapproved=True)
        self.has_unapproved_posts = unapproved_post_qs.exists()

        hidden_post_qs = self.post_set.filter(is_hidden=True)[:1]
        self.has_hidden_posts = hidden_post_qs.exists()

        self.has_events = self.event_set.exists()

        first_post = self.post_set.order_by('id')[:1][0]
        self.set_first_post(first_post)

        last_post_qs = self.post_set.filter(is_unapproved=False).order_by('-id')
        last_post = last_post_qs[:1]
        if last_post:
            self.set_last_post(last_post[0])
        else:
            self.set_last_post(first_post)

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_absolute_url(self, page=1):
        return self.thread_type.get_thread_absolute_url(self, page)

    def get_last_post_url(self):
        return self.thread_type.get_thread_last_post_url(self)

    def get_new_post_url(self):
        return self.thread_type.get_thread_new_post_url(self)

    def get_api_url(self):
        return self.thread_type.get_thread_api_url(self)

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

        self.is_unapproved = post.is_unapproved
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
