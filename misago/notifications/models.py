from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.urls import reverse


NOTIFICATION_SECRET = 16


def get_migration_secret() -> str:
    return get_random_string(NOTIFICATION_SECRET)


class Notification(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # TODO: Move this over to WatchedThread
    secret = models.CharField(
        max_length=NOTIFICATION_SECRET, default=get_migration_secret
    )
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
    read_at = models.DateTimeField(blank=True, null=True)

    def get_absolute_url(self) -> str:
        return reverse("misago:notification", kwargs={"notification_id": self.id})


class WatchedThread(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)

    notifications = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=timezone.now)
