from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse


WATCHED_THREAD_SECRET = 24


def get_watched_thread_secret() -> str:
    return get_random_string(WATCHED_THREAD_SECRET)


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    verb = models.CharField(max_length=32)
    is_read = models.BooleanField(default=False)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    actor_name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        "misago_categories.Category", blank=True, null=True, on_delete=models.CASCADE
    )
    thread = models.ForeignKey(
        "misago_threads.Thread", blank=True, null=True, on_delete=models.CASCADE
    )
    thread_title = models.CharField(max_length=255, blank=True, null=True)
    post = models.ForeignKey(
        "misago_threads.Post", blank=True, null=True, on_delete=models.CASCADE
    )

    # Used instead of repeating notifications, enables messages
    # like "[actor] and X others [verb] [target]"
    extra_actors = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def get_absolute_url(self) -> str:
        return reverse("misago:notification", kwargs={"notification_id": self.id})


class WatchedThread(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)

    notifications = models.PositiveIntegerField(default=0)
    secret = models.CharField(
        max_length=WATCHED_THREAD_SECRET, default=get_watched_thread_secret
    )

    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=timezone.now)