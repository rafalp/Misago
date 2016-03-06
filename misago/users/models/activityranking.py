from django.conf import settings
from django.db import models


class ActivityRanking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    score = models.PositiveIntegerField(default=0, db_index=True)
