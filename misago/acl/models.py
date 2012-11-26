from django.db import models
from django.utils.translation import ugettext_lazy as _

class Role(models.Model):
    """
    Misago User Role model
    """
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255,null=True,blank=True)
    protected = models.BooleanField(default=False)
    
    def __unicode__(self):
        return unicode(_(self.name))
    
    def is_special(self):
        return token