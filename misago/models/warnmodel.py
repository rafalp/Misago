from django.db import models
from misago.signals import rename_user

class Warn(models.Model):
    user = models.ForeignKey('User')
    giver = models.ForeignKey('User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="warnings_given_set")
    giver_name = models.CharField(max_length=255)
    giver_slug = models.SlugField(max_length=255)
    date = models.DateTimeField()
    ip = models.GenericIPAddressField()
    agent = models.CharField(max_length=255)
    reason = models.TextField(null=True, blank=True)
    reason_preparsed = models.TextField(null=True, blank=True)
    canceled = models.BooleanField(default=False)
    canceler = models.ForeignKey('User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="warnings_canceled_set")
    canceler_name = models.CharField(max_length=255, null=True, blank=True)
    canceler_slug = models.SlugField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'misago'


def rename_user_handler(sender, **kwargs):
    Warn.objects.filter(giver=sender).update(
                                             giver_name=sender.username,
                                             giver_slug=sender.username_slug,
                                             )
    Warn.objects.filter(canceler=sender).update(
                                             canceler_name=sender.username,
                                             canceler_slug=sender.username_slug,
                                             )

rename_user.connect(rename_user_handler, dispatch_uid="rename_user_warnings")