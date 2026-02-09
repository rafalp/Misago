from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse

from ..plugins.models import PluginDataModel

WATCHED_THREAD_SECRET = 32


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

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def get_absolute_url(self) -> str:
        return reverse("misago:notification", kwargs={"notification_id": self.id})

    class Meta:
        indexes = [
            models.Index(fields=["-id", "user"]),
            models.Index(fields=["-id", "user", "is_read"]),
            models.Index(
                name="misago_noti_user_unread",
                fields=["user", "is_read"],
                condition=models.Q(is_read=False),
            ),
            models.Index(fields=["user", "post", "is_read"]),
        ]


class WatchedThread(PluginDataModel):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)

    send_emails = models.BooleanField(default=True)
    secret = models.CharField(
        max_length=WATCHED_THREAD_SECRET, default=get_watched_thread_secret
    )

    created_at = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = PluginDataModel.Meta.indexes + [
            models.Index(fields=["user", "-thread"]),
        ]

    def get_disable_emails_url(self):
        return reverse(
            "misago:notifications-disable-email",
            kwargs={
                "watched_thread_id": self.id,
                "secret": self.secret,
            },
        )
