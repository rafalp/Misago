from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..conf import settings

CACHE_KEY = "misago_agreements"


class AgreementManager(models.Manager):
    def invalidate_cache(self):
        cache.delete(CACHE_KEY)

    def get_agreements(self):
        agreements = self.get_agreements_from_cache()
        if agreements == "nada":
            agreements = self.get_agreements_from_db()
            cache.set(CACHE_KEY, agreements)
        return agreements

    def get_agreements_from_cache(self):
        return cache.get(CACHE_KEY, "nada")

    def get_agreements_from_db(self):
        agreements = {}
        for agreement in Agreement.objects.filter(is_active=True):
            agreements[agreement.type] = {
                "id": agreement.id,
                "title": agreement.get_final_title(),
                "link": agreement.link,
                "text": bool(agreement.text),
            }
        return agreements


class Agreement(models.Model):
    TYPE_TOS = "terms_of_service"
    TYPE_PRIVACY = "privacy_policy"
    TYPE_CHOICES = [
        (TYPE_TOS, _("Terms of service")),
        (TYPE_PRIVACY, _("Privacy policy")),
    ]

    type = models.CharField(
        max_length=20, default=TYPE_TOS, choices=TYPE_CHOICES, db_index=True
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    created_by_name = models.CharField(max_length=255, null=True, blank=True)
    last_modified_on = models.DateTimeField(null=True, blank=True)
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    last_modified_by_name = models.CharField(max_length=255, null=True, blank=True)

    objects = AgreementManager()

    def get_absolute_url(self):
        if not self.is_active:
            return None

        if self.link:
            return self.link

        if self.type == self.TYPE_TOS:
            return reverse("misago:terms-of-service")

        return reverse("misago:privacy-policy")

    def get_final_title(self):
        return self.title or self.get_type_display()

    def set_created_by(self, user):
        self.created_by = user
        self.created_by_name = user.username

    def set_last_modified_by(self, user):
        self.last_modified_by = user
        self.last_modified_by_name = user.username


class UserAgreement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    agreement = models.ForeignKey(
        Agreement, related_name="accepted_by", on_delete=models.CASCADE
    )
    accepted_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-pk"]
