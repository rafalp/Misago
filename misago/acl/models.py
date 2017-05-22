from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from . import version as acl_version


def permissions_default():
    return {}


@python_2_unicode_compatible
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
            acl_version.invalidate()
        return super(BaseRole, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        acl_version.invalidate()
        return super(BaseRole, self).delete(*args, **kwargs)


class Role(BaseRole):
    pass
