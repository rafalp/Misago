from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..users.enums import DefaultGroupId
from .moderator import ModeratorPermissions

if TYPE_CHECKING:
    from ..users.models import User


class CategoryGroupPermission(models.Model):
    category = models.ForeignKey("misago_categories.Category", on_delete=models.CASCADE)
    group = models.ForeignKey("misago_users.Group", on_delete=models.CASCADE)
    permission = models.CharField(max_length=32)


class ModeratorManager(models.Manager):
    def get_moderator_permissions(self, user: "User") -> ModeratorPermissions:
        fin_is_global: bool = False
        fin_categories: list[int] = []
        fin_private_threads: bool = False

        queryset = Moderator.objects.filter(
            models.Q(group__in=user.groups_ids) | models.Q(user=user)
        ).values_list("is_global", "categories", "private_threads")

        for is_global, categories, private_threads in queryset:
            fin_is_global = fin_is_global or is_global
            fin_categories += categories
            fin_private_threads = fin_private_threads or private_threads

        return ModeratorPermissions(
            is_global=fin_is_global,
            categories_ids=set(fin_categories),
            private_threads=fin_private_threads,
        )


class Moderator(models.Model):
    group = models.ForeignKey("misago_users.Group", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE
    )

    is_global = models.BooleanField(default=True)
    categories = ArrayField(models.PositiveIntegerField(), default=list)
    private_threads = models.BooleanField(default=False)

    objects = ModeratorManager()

    @property
    def is_protected(self):
        return self.group_id in (DefaultGroupId.ADMINS, DefaultGroupId.MODERATORS)

    @property
    def name(self):
        if self.group_id:
            return str(self.group)
        return str(self.user)
