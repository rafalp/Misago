from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext as _

from .cache import clear_acl_cache


def permissions_default():
    return {}


class BaseRole(models.Model):
    name = models.CharField(max_length=255)
    special_role = models.CharField(max_length=255, null=True, blank=True)
    permissions = JSONField(default=permissions_default)

    class Meta:
        abstract = True

    def __str__(self):
        return _(self.name)

    def save(self, *args, **kwargs):
        if self.pk:
            clear_acl_cache()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        clear_acl_cache()
        return super().delete(*args, **kwargs)


class Role(BaseRole):
    pass
