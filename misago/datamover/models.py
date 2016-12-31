from django.db import models


class MovedId(models.Model):
    model = models.CharField(max_length=255)
    old_id = models.CharField(max_length=255)
    new_id = models.CharField(max_length=255)
