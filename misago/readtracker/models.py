from django.conf import settings
from django.db import models
from django.utils import timezone


class CategoryRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    last_read_on = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        from misago.core import deprecations
        deprecations.warn("CategoryRead has been deprecated")
        super(CategoryRead, self).__init__(*args, **kwargs)


class ThreadRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        'misago_threads.Thread',
        on_delete=models.CASCADE,
    )
    last_read_on = models.DateTimeField()

    def __init__(self, *args, **kwargs):
        from misago.core import deprecations
        deprecations.warn("ThreadRead has been deprecated")
        super(ThreadRead, self).__init__(*args, **kwargs)


class PostRead(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        'misago_categories.Category',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        'misago_threads.Thread',
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'misago_threads.Post',
        on_delete=models.CASCADE,
    )
    last_read_on = models.DateTimeField(default=timezone.now)
