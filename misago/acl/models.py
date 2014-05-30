from django.db import models
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.acl import cachebuster
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Role(models.Model):
    name = models.CharField(max_length=255)
    pickled_permissions = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(_(self.name))

    def save(self, *args, **kwargs):
        if self.pk:
            cachebuster.invalidate()
        return super(Role, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cachebuster.invalidate()
        return super(Role, self).delete(*args, **kwargs)

    @property
    def permissions(self):
        try:
            return self.permissions_cache
        except AttributeError:
            try:
                self.permissions_cache = pickle.loads(
                    base64.decodestring(self.pickled_permissions))
            except Exception:
                self.permissions_cache = {}
        return self.permissions_cache

    @permissions.setter
    def permissions(self, permissions):
        self.permissions_cache = permissions
        self.pickled_permissions = base64.encodestring(
            pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))


class ForumRole(models.Model):
    name = models.CharField(max_length=255)
    pickled_permissions = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return unicode(_(self.name))

    def save(self, *args, **kwargs):
        if self.pk:
            cachebuster.invalidate()
        return super(ForumRole, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cachebuster.invalidate()
        return super(ForumRole, self).delete(*args, **kwargs)

    @property
    def permissions(self):
        try:
            return self.permissions_cache
        except AttributeError:
            try:
                self.permissions_cache = pickle.loads(
                    base64.decodestring(self.pickled_permissions))
            except Exception:
                self.permissions_cache = {}
        return self.permissions_cache

    @permissions.setter
    def permissions(self, permissions):
        self.permissions_cache = permissions
        self.pickled_permissions = base64.encodestring(
            pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))


"""register models in misago admin"""
site.add_node(
    parent='misago:admin',
    after='misago:admin:users:accounts:index',
    namespace='misago:admin:permissions',
    link='misago:admin:permissions:users:index',
    name=_("Permissions"),
    icon='fa fa-adjust')

site.add_node(
    parent='misago:admin:permissions',
    namespace='misago:admin:permissions:users',
    link='misago:admin:permissions:users:index',
    name=_("User Roles"),
    icon='fa fa-th-large')

site.add_node(
    parent='misago:admin:permissions',
    namespace='misago:admin:permissions:forums',
    link='misago:admin:permissions:forums:index',
    name=_("Forum Roles"),
    icon='fa fa-list')
