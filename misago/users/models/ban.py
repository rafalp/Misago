from datetime import timedelta
import re

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.core import cachebuster


__all__ = [
    'BAN_USERNAME', 'BAN_EMAIL', 'BAN_IP', 'BANS_CHOICES', 'Ban', 'BanCache'
]


BAN_CACHEBUSTER = 'misago_bans'


BAN_USERNAME = 0
BAN_EMAIL = 1
BAN_IP = 2


BANS_CHOICES = (
    (BAN_USERNAME, _('Username')),
    (BAN_EMAIL, _('E-mail address')),
    (BAN_IP, _('IP address')),
)


class BansManager(models.Manager):
    def is_ip_banned(self, ip):
        return self.check_ban(ip=ip)

    def is_username_banned(self, username):
        return self.check_ban(username=username)

    def is_email_banned(self, email):
        return self.check_ban(email=email)

    def invalidate_cache(self):
        cachebuster.invalidate(BAN_CACHEBUSTER)

    def find_ban(self, username=None, email=None, ip=None):
        tests = []

        if username:
            username = username.lower()
            tests.append(BAN_USERNAME)
        if email:
            email = email.lower()
            tests.append(BAN_EMAIL)
        if ip:
            tests.append(BAN_IP)

        queryset = self.filter(is_valid=True)
        if len(tests) == 1:
            queryset = queryset.filter(test=tests[0])
        elif tests:
            queryset = queryset.filter(test__in=tests)

        for ban in queryset.order_by('-id').iterator():
            if (ban.test == BAN_USERNAME and username and
                    ban.test_value(username)):
                return ban
            elif ban.test == BAN_EMAIL and email and ban.test_value(email):
                return ban
            elif ban.test == BAN_IP and ip and ban.test_value(ip):
                return ban
        else:
            raise Ban.DoesNotExist('no valid ban for values has been found')


class Ban(models.Model):
    test = models.PositiveIntegerField(default=BAN_USERNAME, db_index=True)
    banned_value = models.CharField(max_length=255, db_index=True)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True, db_index=True)
    is_valid = models.BooleanField(default=True, db_index=True)

    objects = BansManager()

    def save(self, *args, **kwargs):
        self.banned_value = self.banned_value.lower()
        self.is_valid = not self.is_expired

        return super(Ban, self).save(*args, **kwargs)

    @property
    def test_name(self):
        return BANS_CHOICES[self.test][1]

    @property
    def name(self):
        return self.banned_value

    @property
    def is_expired(self):
        if self.valid_until:
            return self.valid_until < timezone.now().date()
        else:
            return False

    def test_value(self, value):
        if '*' in self.banned_value:
            regex = re.escape(self.banned_value).replace('\*', '(.*?)')
            return re.search('^%s$' % regex, value) is not None
        else:
            return self.banned_value == value

    def lift(self):
        self.valid_until = (timezone.now() - timedelta(days=1)).date()


class BanCache(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, related_name='ban_cache')
    ban = models.ForeignKey(
        Ban, null=True, blank=True, on_delete=models.SET_NULL)
    bans_version = models.PositiveIntegerField(default=0)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    @property
    def is_banned(self):
        return bool(self.ban)

    @property
    def is_valid(self):
        version_is_valid = cachebuster.is_valid(BAN_CACHEBUSTER,
                                                self.bans_version)
        date_today = timezone.now().date()
        not_expired = not self.valid_until or self.valid_until > date_today

        return version_is_valid and not_expired
