from django.db import models
from django.utils.translation import ugettext as _
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
