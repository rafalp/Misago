from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.conf import settings


class NoActiveLegalAgreement(ValidationError):
    pass


class LegalAgreementManager(models.Manager):
    def get_current(self):
        try:
            return self.filter(is_active=True)
        except self.model.DoesNotExist:
            raise NoActiveLegalAgreement(
                u'Please create an active LegalAgreement'
            )


class LegalAgreement(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    key = models.SlugField(unique=True, blank=True)

    TOS = 'terms_of_service'
    PRIVACY = 'privacy_policy'
    LEGAL_CHOICES = (
        (TOS, 'Terms of service'),
        (PRIVACY, 'Privacy Policy'),
    )
    title = models.CharField(
        max_length=20,
        choices=LEGAL_CHOICES,
        default=TOS
    )
    text = models.TextField(
        verbose_name=_('content'),
        blank=True
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('active/publish'),
        help_text=_(
            u'Only one terms of service is allowed to be active'
        )
    )

    objects = LegalAgreementManager()

    def __init__(self, *args, **kwargs):
        super(LegalAgreement, self).__init__(*args, **kwargs)
        self.old_is_active = self.is_active

    def __str__(self):
        return self.title + "-" + self.created_at.strftime("%Y-%m-%d")

    def has_user_agreed_latest_legal(self, user, legal):
        return UserAgreementAcceptance.objects.filter(
            legal_agreement=LegalAgreement.objects.get_current().get(title=legal),
            user=user,
        ).exists()

    def accept(self, user):
        acceptance = UserAgreementAcceptance(
            legal_agreement=LegalAgreement.objects.get_current().get(title=self.title), user=user)
        acceptance.save()

    def save(self, *args, **kwargs):
        """ Ensure that one LegalAgreement is active"""
        if  self.is_active:
            LegalAgreement.objects.exclude(id=self.id).filter(title=self.title).update(is_active=False)
        else:
            if not LegalAgreement.objects.exclude(id=self.id).filter(is_active=True, title=self.title).exists():
                raise NoActiveLegalAgreement(
                    u'One of the {} must be marked active'.format(self.title)
                )

        # Set the latest published date.
        if self.old_is_active != self.is_active and self.is_active:
            self.published_at = timezone.now()

        self.key = slugify(self.title + " " + self.created_at.strftime("%Y-%m-%d"))
        super(LegalAgreement, self).save(*args, **kwargs)


class UserAgreementAcceptance(models.Model):
    accepted_on = models.DateTimeField(auto_now=True)
    has_accepted = models.BooleanField(default=False)
    user_ip = models.GenericIPAddressField()
    legal_agreement = models.ForeignKey(LegalAgreement, related_name='legal_agreement')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='user_agreement'
    )

    def __str__(self):
        return '%s accepted %s (published at %s) on %s' % (
            self.user, self.legal_agreement.title, self.legal_agreement.published_at, self.accepted_on)

    class Meta:
        unique_together = (
            'user',
            'legal_agreement',
            'accepted_on',
        )
        ordering = ["-accepted_on"]
