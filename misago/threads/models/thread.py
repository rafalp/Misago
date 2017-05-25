from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings
from misago.core.pgutils import PgPartialIndex
from misago.core.utils import slugify


@python_2_unicode_compatible
class Thread(models.Model):
    WEIGHT_DEFAULT = 0
    WEIGHT_PINNED = 1
    WEIGHT_GLOBAL = 2

    WEIGHT_CHOICES = [
        (WEIGHT_DEFAULT, _("Don't pin thread")),
        (WEIGHT_PINNED, _("Pin thread within category")),
        (WEIGHT_GLOBAL, _("Pin thread globally")),
    ]

    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    replies = models.PositiveIntegerField(default=0, db_index=True)

    has_events = models.BooleanField(default=False)
    has_poll = models.BooleanField(default=False)
    has_reported_posts = models.BooleanField(default=False)
    has_open_reports = models.BooleanField(default=False)
    has_unapproved_posts = models.BooleanField(default=False)
    has_hidden_posts = models.BooleanField(default=False)

    started_on = models.DateTimeField(db_index=True)
    last_post_on = models.DateTimeField(db_index=True)

    first_post = models.ForeignKey(
        'misago_threads.Post',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    starter_name = models.CharField(max_length=255)
    starter_slug = models.CharField(max_length=255)

    last_post = models.ForeignKey(
        'misago_threads.Post',
        related_name='+',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    last_post_is_event = models.BooleanField(default=False)
    last_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='last_poster_set',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    last_poster_name = models.CharField(max_length=255, null=True, blank=True)
    last_poster_slug = models.CharField(max_length=255, null=True, blank=True)

    weight = models.PositiveIntegerField(default=WEIGHT_DEFAULT)

    is_unapproved = models.BooleanField(default=False, db_index=True)
    is_hidden = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='privatethread_set',
        through='ThreadParticipant',
        through_fields=('thread', 'user'),
    )

    class Meta:
        indexes = [
            PgPartialIndex(
                fields=['weight'],
                where={'weight': 2},
            ),
            PgPartialIndex(
                fields=['weight'],
                where={'weight': 1},
            ),
            PgPartialIndex(
                fields=['weight'],
                where={'weight': 0},
            ),
            PgPartialIndex(
                fields=['weight'],
                where={'weight__lt': 2},
            ),
            PgPartialIndex(
                fields=['has_reported_posts'],
                where={'has_reported_posts': True},
            ),
            PgPartialIndex(
                fields=['has_unapproved_posts'],
                where={'has_unapproved_posts': True},
            ),
            PgPartialIndex(
                fields=['is_hidden'],
                where={'is_hidden': False},
            ),
        ]

        index_together = [
            ['category', 'id'],
            ['category', 'last_post_on'],
            ['category', 'replies'],
        ]

    def __str__(self):
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
        try:
            self.has_poll = bool(self.poll)
        except ObjectDoesNotExist:
            self.has_poll = False

        self.replies = self.post_set.filter(is_event=False, is_unapproved=False).count()

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

        posts = self.post_set.order_by('id')

        first_post = posts.first()
        self.set_first_post(first_post)

        last_post = posts.filter(is_unapproved=False).last()
        if last_post:
            self.set_last_post(last_post)
        else:
            self.set_last_post(first_post)

        self.has_events = False
        if last_post:
            if last_post.is_event:
                self.has_events = True
            else:
                self.has_events = self.post_set.filter(is_event=True).exists()

    @property
    def thread_type(self):
        return self.category.thread_type

    def get_api_url(self):
        return self.thread_type.get_thread_api_url(self)

    def get_editor_api_url(self):
        return self.thread_type.get_thread_editor_api_url(self)

    def get_merge_api_url(self):
        return self.thread_type.get_thread_merge_api_url(self)

    def get_posts_api_url(self):
        return self.thread_type.get_thread_posts_api_url(self)

    def get_post_merge_api_url(self):
        return self.thread_type.get_post_merge_api_url(self)

    def get_post_move_api_url(self):
        return self.thread_type.get_post_move_api_url(self)

    def get_post_split_api_url(self):
        return self.thread_type.get_post_split_api_url(self)

    def get_poll_api_url(self):
        return self.thread_type.get_thread_poll_api_url(self)

    def get_absolute_url(self, page=1):
        return self.thread_type.get_thread_absolute_url(self, page)

    def get_new_post_url(self):
        return self.thread_type.get_thread_new_post_url(self)

    def get_last_post_url(self):
        return self.thread_type.get_thread_last_post_url(self)

    def get_unapproved_post_url(self):
        return self.thread_type.get_thread_unapproved_post_url(self)

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
        self.last_post_is_event = post.is_event
        self.last_post = post
        self.last_poster = post.poster
        self.last_poster_name = post.poster_name
        if post.poster:
            self.last_poster_slug = post.poster.slug
        else:
            self.last_poster_slug = slugify(post.poster_name)
