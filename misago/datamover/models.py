from django.db import models


class MovedId(models.Model):
    model = models.CharField(max_length=255)
    old_id = models.CharField(max_length=255)
    new_id = models.CharField(max_length=255)


class OldIdRedirect(models.Model):
    ATTACHMENT = 0
    CATEGORY = 1
    POST = 2
    THREAD = 3
    USER = 4

    model = models.PositiveIntegerField()
    old_id = models.PositiveIntegerField()
    new_id = models.PositiveIntegerField()

    class Meta:
        index_together = [
            ['model', 'old_id'],
        ]
