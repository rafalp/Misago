import re

from django.conf import settings
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .. import BANS_CACHE
from ...cache.versions import invalidate_cache


class BansManager(models.Manager):
    def get_ip_ban(self, ip, registration_only=False):
        return self.get_ban(ip=ip, registration_only=registration_only)

    def get_username_ban(self, username, registration_only=False):
        return self.get_ban(username=username, registration_only=registration_only)

    def get_email_ban(self, email, registration_only=False):
        return self.get_ban(email=email, registration_only=registration_only)

    def invalidate_cache(self):
        invalidate_cache(BANS_CACHE)

    def get_ban(self, username=None, email=None, ip=None, registration_only=False):
        checks = []

        if username:
            username = username.lower()
            checks.append(self.model.USERNAME)
        if email:
            email = email.lower()
            checks.append(self.model.EMAIL)
        if ip:
            checks.append(self.model.IP)

        queryset = self.filter(is_checked=True)
        if not registration_only:
            queryset = self.filter(registration_only=False)

        if len(checks) == 1:
            queryset = queryset.filter(check_type=checks[0])
        elif checks:
            queryset = queryset.filter(check_type__in=checks)

        for ban in queryset.order_by("-id").iterator():
            if ban.is_expired:
                continue
            elif (
                ban.check_type == self.model.USERNAME
                and username
                and ban.check_value(username)
            ):
                return ban
            elif (
                ban.check_type == self.model.EMAIL and email and ban.check_value(email)
            ):
                return ban
            elif ban.check_type == self.model.IP and ip and ban.check_value(ip):
                return ban

        raise Ban.DoesNotExist("specified values are not banned")


class Ban(models.Model):
    USERNAME = 0
    EMAIL = 1
    IP = 2

    CHOICES = [
        (USERNAME, _("Username")),
        (EMAIL, _("E-mail address")),
        (IP, _("IP address")),
    ]

    check_type = models.PositiveIntegerField(
        default=USERNAME, choices=CHOICES, db_index=True
    )
    registration_only = models.BooleanField(default=False, db_index=True)
    banned_value = models.CharField(max_length=255, db_index=True)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True, db_index=True)
    is_checked = models.BooleanField(default=True, db_index=True)

    objects = BansManager()

    def save(self, *args, **kwargs):
        self.banned_value = self.banned_value.lower()
        self.is_checked = not self.is_expired

        return super().save(*args, **kwargs)

    def get_serialized_message(self):
        from ..serializers import BanMessageSerializer

        return BanMessageSerializer(self).data

    @property
    def name(self):
        return self.banned_value

    @property
    def is_expired(self):
        if self.expires_on:
            return self.expires_on < timezone.now()
        return False

    def check_value(self, value):
        if "*" in self.banned_value:
            regex = re.escape(self.banned_value).replace(r"\*", r"(.*?)")
            return re.search("^%s$" % regex, value, re.IGNORECASE) is not None
        return self.banned_value.lower() == value.lower()

    def lift(self):
        self.expires_on = timezone.now()


class BanCache(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name="ban_cache",
        on_delete=models.CASCADE,
    )
    ban = models.ForeignKey(Ban, null=True, blank=True, on_delete=models.SET_NULL)
    cache_version = models.CharField(max_length=8)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            pass  # first come is first serve with ban cache

    def get_serialized_message(self):
        from ..serializers import BanMessageSerializer

        temp_ban = Ban(
            id=1,
            check_type=Ban.USERNAME,
            user_message=self.user_message,
            staff_message=self.staff_message,
            expires_on=self.expires_on,
        )
        return BanMessageSerializer(temp_ban).data

    @property
    def is_banned(self):
        return bool(self.ban)

    def is_valid(self, cache_versions):
        is_versioned = self.cache_version == cache_versions[BANS_CACHE]
        is_expired = self.expires_on and self.expires_on < timezone.now()

        return is_versioned and not is_expired
