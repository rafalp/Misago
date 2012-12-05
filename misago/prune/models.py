from django.db import models

class Policy(models.Model):
    """
    Pruning policy
    """
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,null=True,blank=True)
    posts = models.PositiveIntegerField(default=0)
    registered = models.PositiveIntegerField(default=0)
    last_visit = models.PositiveIntegerField(default=0)
    