from django.db import models
from django.utils import timezone

from ..conf import settings


class Subject(models.Model):
    sub = models.CharField(max_length=36, primary_key=True)  # UUID4 str length
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    last_used_on = models.DateTimeField(default=timezone.now)
