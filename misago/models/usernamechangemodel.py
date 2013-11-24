from django.db import models

class UsernameChange(models.Model):
    user = models.ForeignKey('User', related_name='namechanges')
    date = models.DateTimeField()
    old_username = models.CharField(max_length=255)

    class Meta:
        app_label = 'misago'