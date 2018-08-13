from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings


class Agreement(models.Model):
    TYPE_TOS = 'terms-of-service'
    TYPE_PRIVACY = 'privacy-policy'
    TYPE_CHOICES = [
        (TYPE_TOS, _('Terms of service')),
        (TYPE_PRIVACY, _('Privacy Policy')),
    ]

    type = models.CharField(
        max_length=20,
        default=TYPE_TOS,
        choices=TYPE_CHOICES,
        db_index=True,
    )
    version = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='+',
    )
    created_by_name = models.CharField(max_length=255, null=True, blank=True)
    last_modified_on = models.DateTimeField(default=timezone.now)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='+',
    )
    last_modified_by_name = models.CharField(max_length=255, null=True, blank=True)


class UserAgreement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='agreements'
    )
    agreement = models.ForeignKey(Agreement, related_name='agreements')
    accepted_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-accepted_on"]