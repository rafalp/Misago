from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..users.enums import DefaultGroupId

if TYPE_CHECKING:
    from ..users.models import User


class CategoryGroupPermission(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", on_delete=models.CASCADE)
    permission = models.CharField(max_length=32)


class ModeratorManager(models.Manager):
    def moderated_categories_ids(self, user: "User") -> list[int]:
        all_categories: list[int] = []
        queryset = Moderator.objects.filter(
            models.Q(group__in=user.groups_ids) | models.Q(user=user)
        ).values_list("categories", flat=True)

        for categories in queryset:
            all_categories += categories

        return list(set(all_categories))


class Moderator(models.Model):
    group = models.ForeignKey("misago_users.Group", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )

    is_global = models.BooleanField(default=True)

    categories = ArrayField(models.PositiveIntegerField(), default=list)

    objects = ModeratorManager()

    @property
    def is_protected(self):
        return self.group_id in (DefaultGroupId.ADMINS, DefaultGroupId.MODERATORS)

    @property
    def name(self):
        if self.group_id:
            return str(self.group)
        return str(self.user)
