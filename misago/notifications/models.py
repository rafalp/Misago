from django.conf import settings
from django.db import models


class Notification(models.Model):
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
    post = models.ForeignKey(
        "misago_threads.Post", blank=True, null=True, on_delete=models.CASCADE
    )

    # Used instead of repeating notifications, enables messages
    # like "[actor] and X others [verb] [target]"
    extra_actors = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_created=True, db_index=True)
    read_at = models.DateTimeField(blank=True, null=True)


class WatchedThread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    thread = models.ForeignKey("misago_threads.Thread", on_delete=models.CASCADE)

    send_email = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_created=True)
    read_at = models.DateTimeField()
