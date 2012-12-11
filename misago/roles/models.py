from django.db import models
from django.utils.translation import ugettext_lazy as _
import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Role(models.Model):
    """
    Misago User Role model
    """
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255,null=True,blank=True)
    protected = models.BooleanField(default=False)
    permissions = models.TextField(null=True,blank=True)
    permissions_cache = {}
    
    def __unicode__(self):
        return unicode(_(self.name))
    
    def is_special(self):
        return token
    
    def get_permissions(self):
        if self.permissions_cache:
            return self.permissions_cache
        
        try:
            self.permissions_cache = pickle.loads(base64.decodestring(self.permissions))
        except Exception:
            # ValueError, SuspiciousOperation, unpickling exceptions. If any of
            # these happen, just return an empty dictionary (an empty permissions list).
            self.permissions_cache = {}
            
        return self.permissions_cache
    
    def set_permissions(self, permissions):
        self.permissions_cache = permissions
        self.permissions = base64.encodestring(pickle.dumps(permissions, pickle.HIGHEST_PROTOCOL))