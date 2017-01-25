from django.db import models


class MovedId(models.Model):
    model = models.CharField(max_length=255)
    old_id = models.CharField(max_length=255)
    new_id = models.CharField(max_length=255)


class OldIdRedirect(models.Model):
    CATEGORY = 0
    POST = 1
    THREAD = 2
    USER = 3

    model = models.PositiveIntegerField()
    old_id = models.PositiveIntegerField()
    new_id = models.PositiveIntegerField()

    class Meta:
        index_together = [
            ['model', 'old_id'],
        ]
