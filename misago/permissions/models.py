from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..users.enums import DefaultGroupId


class CategoryGroupPermission(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", on_delete=models.CASCADE)
    permission = models.CharField(max_length=32)


class Moderator(models.Model):
    group = models.ForeignKey("misago_users.Group", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )

    is_global = models.BooleanField(default=True)

    categories = ArrayField(models.PositiveIntegerField(), default=list)

    @property
    def is_protected(self):
        return self.group_id in (DefaultGroupId.ADMINS, DefaultGroupId.MODERATORS)

    @property
    def name(self):
        if self.group_id:
            return str(self.group)
        return str(self.user)
