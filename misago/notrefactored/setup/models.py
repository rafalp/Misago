from django.db import models

class Fixture(models.Model):
    app_name = models.CharField(max_length=255)