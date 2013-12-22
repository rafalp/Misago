from django.db import models

class Warn(models.Model):
    user = models.ForeignKey('User')
    giver = models.ForeignKey('User', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="warnings_given_set")
    giver_name = models.CharField(max_length=255)
    giver_slug = models.SlugField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    reason_user = models.TextField()
    reason_team = models.TextField(null=True, blank=True)
    canceled = models.BooleanField(default=False)

    class Meta:
        app_label = 'misago'
