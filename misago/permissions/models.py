from dataclasses import dataclass
from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..users.enums import DefaultGroupId
from .moderatordata import ModeratorData

if TYPE_CHECKING:
    from ..users.models import User


class CategoryGroupPermission(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", on_delete=models.CASCADE)
    permission = models.CharField(max_length=32)


@dataclass(frozen=True)
class ModeratorData:
    is_global: bool
    categories_ids: set[int]


class ModeratorManager(models.Manager):
    def get_moderator_data(self, user: "User") -> ModeratorData:
        mod_is_global: bool = False
        mod_categories: list[int] = []

        queryset = Moderator.objects.filter(
            models.Q(group__in=user.groups_ids) | models.Q(user=user)
        ).values_list("is_global", "categories")

        for is_global, categories in queryset:
            mod_is_global = mod_is_global or is_global
            mod_categories += categories

        return ModeratorData(
            is_global=mod_is_global,
            categories_ids=set(mod_categories),
        )


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
