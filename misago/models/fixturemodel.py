from django.db import models

class Fixture(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'misago'