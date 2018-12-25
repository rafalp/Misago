from django.conf import settings
from django.db import IntegrityError, models
from django.utils import timezone


class Online(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name="online_tracker",
        on_delete=models.CASCADE,
    )
    last_click = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            pass  # first come is first serve in online tracker
