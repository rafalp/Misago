from django.db import models

BAN_NAME_EMAIL = 0
BAN_NAME = 1
BAN_EMAIL = 2
BAN_IP = 3


class Ban(models.Model):
    test = models.PositiveIntegerField(default=BAN_NAME_EMAIL)
    ban = models.CharField(max_length=255)
    reason_user = models.TextField(null=True, blank=True)
    reason_admin = models.TextField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = 'misago'