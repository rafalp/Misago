from django.db import models
from django.dispatch import receiver

from misago.core import serializer

from misago.acl import version as acl_version
from misago.core.signals import secret_key_changed


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
            if self.pickled_permissions:
                self.permissions_cache = serializer.loads(
                    self.pickled_permissions)
            else:
                self.permissions_cache = {}
        return self.permissions_cache

    @permissions.setter
    def permissions(self, permissions):
        self.permissions_cache = permissions
        self.pickled_permissions = serializer.dumps(permissions)


class Role(BaseRole):
    pass


"""
Signal handlers
"""
@receiver(secret_key_changed)
def update_roles_pickles(sender, **kwargs):
    for role in Role.objects.iterator():
        if role.pickled_permissions:
            role.pickled_permissions = serializer.regenerate_checksum(
                role.pickled_permissions)
            role.save(update_fields=['pickled_permissions'])
