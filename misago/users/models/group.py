from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=150, unique=True)

    ordering = models.PositiveIntegerField(default=0)

    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        ordering = ["ordering"]
