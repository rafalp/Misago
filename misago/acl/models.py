from django.db import models

class Role(models.Model):
    """
    Misago User Role model
    """
    name = models.CharField(max_length=255)
    token = models.CharField(max_length=255,null=True,blank=True)
    
    def is_special(self):
        return token