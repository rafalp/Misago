from django.db import models
from misago.signals import rename_user

class Warn(models.Model):
    user = models.ForeignKey('User', related_name="warning_set")
    reason = models.TextField(null=True, blank=True)
    reason_preparsed = models.TextField(null=True, blank=True)
    given_on = models.DateTimeField()
    giver = models.ForeignKey('User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="warnings_given_set")
    giver_username = models.CharField(max_length=255)
    giver_slug = models.SlugField(max_length=255)
    giver_ip = models.GenericIPAddressField()
    giver_agent = models.CharField(max_length=255)
    canceled = models.BooleanField(default=False)
    canceled_on = models.DateTimeField(null=True, blank=True)
    canceler = models.ForeignKey('User', null=True, blank=True,
        on_delete=models.SET_NULL, related_name="warnings_canceled_set")
    canceler_username = models.CharField(max_length=255, null=True, blank=True)
    canceler_slug = models.SlugField(max_length=255, null=True, blank=True)
    canceler_ip = models.GenericIPAddressField(null=True, blank=True)
    canceler_agent = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'misago'


def rename_user_handler(sender, **kwargs):
    Warn.objects.filter(giver=sender).update(
                                             giver_username=sender.username,
                                             giver_slug=sender.username_slug,
                                             )
    Warn.objects.filter(canceler=sender).update(
                                             canceler_username=sender.username,
                                             canceler_slug=sender.username_slug,
                                             )
rename_user.connect(rename_user_handler, dispatch_uid="rename_user_warnings")