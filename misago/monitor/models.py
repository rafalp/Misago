from django.db import models

class Item(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    value = models.TextField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)