from django.db import models

from misago.core import serializer

from misago.acl import version as acl_version


class BaseRole(models.Model):
    name = models.CharField(max_length=255)
    special_role = models.CharField(max_length=255, null=True, blank=True)
    pickled_permissions = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            acl_version.invalidate()
        return super(BaseRole, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        acl_version.invalidate()
        return super(BaseRole, self).delete(*args, **kwargs)

    @property
    def permissions(self):
        try:
            return self.permissions_cache
        except AttributeError:
            try:
                self.permissions_cache = serializer.loads(
                    self.pickled_permissions)
            except Exception:
                self.permissions_cache = {}
        return self.permissions_cache

    @permissions.setter
    def permissions(self, permissions):
        self.permissions_cache = permissions
        self.pickled_permissions = serializer.dumps(permissions)


class Role(BaseRole):
    pass
