import re

from django.conf import settings
from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from misago.core import cachebuster


__all__ = [
    'BAN_USERNAME', 'BAN_EMAIL', 'BAN_IP', 'BANS_CHOICES',
    'Ban', 'BanCache'
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
    def get_ip_ban(self, ip):
        return self.get_ban(ip=ip)

    def get_username_ban(self, username):
        return self.get_ban(username=username)

    def get_email_ban(self, email):
        return self.get_ban(email=email)

    def invalidate_cache(self):
        cachebuster.invalidate(BAN_CACHEBUSTER)

    def get_ban(self, username=None, email=None, ip=None):
        checks = []

        if username:
            username = username.lower()
            checks.append(BAN_USERNAME)
        if email:
            email = email.lower()
            checks.append(BAN_EMAIL)
        if ip:
            checks.append(BAN_IP)

        queryset = self.filter(is_checked=True)
        if len(checks) == 1:
            queryset = queryset.filter(check_type=checks[0])
        elif checks:
            queryset = queryset.filter(check_type__in=checks)

        for ban in queryset.order_by('-id').iterator():
            if ban.is_expired:
                continue
            elif (ban.check_type == BAN_USERNAME and username and
                    ban.check_value(username)):
                return ban
            elif (ban.check_type == BAN_EMAIL and email and
                    ban.check_value(email)):
                return ban
            elif ban.check_type == BAN_IP and ip and ban.check_value(ip):
                return ban
        else:
            raise Ban.DoesNotExist('specified values are not banned')


class Ban(models.Model):
    check_type = models.PositiveIntegerField(default=BAN_USERNAME, db_index=True)
    banned_value = models.CharField(max_length=255, db_index=True)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True, db_index=True)
    is_checked = models.BooleanField(default=True, db_index=True)

    objects = BansManager()

    def save(self, *args, **kwargs):
        self.banned_value = self.banned_value.lower()
        self.is_checked = not self.is_expired

        return super(Ban, self).save(*args, **kwargs)

    def get_serialized_message(self):
        from misago.users.serializers import BanMessageSerializer
        return BanMessageSerializer(self).data

    @property
    def check_name(self):
        return BANS_CHOICES[self.check_type][1]

    @property
    def name(self):
        return self.banned_value

    @property
    def is_expired(self):
        if self.expires_on:
            return self.expires_on < timezone.now()
        else:
            return False

    def check_value(self, value):
        if '*' in self.banned_value:
            regex = re.escape(self.banned_value).replace('\*', '(.*?)')
            return re.search('^%s$' % regex, value) is not None
        else:
            return self.banned_value == value

    def lift(self):
        self.expires_on = timezone.now()


class BanCache(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, related_name='ban_cache')
    ban = models.ForeignKey(Ban, null=True, blank=True, on_delete=models.SET_NULL)
    bans_version = models.PositiveIntegerField(default=0)
    user_message = models.TextField(null=True, blank=True)
    staff_message = models.TextField(null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            super(BanCache, self).save(*args, **kwargs)
        except IntegrityError:
            pass # first come is first serve with ban cache

    def get_serialized_message(self):
        from misago.users.serializers import BanMessageSerializer
        temp_ban = Ban(
            id=1,
            check_type=BAN_USERNAME,
            user_message=self.user_message,
            staff_message=self.staff_message,
            expires_on=self.expires_on
        )
        return BanMessageSerializer(temp_ban).data

    @property
    def is_banned(self):
        return bool(self.ban)

    @property
    def is_valid(self):
        version_is_valid = cachebuster.is_valid(BAN_CACHEBUSTER,
                                                self.bans_version)
        expired = self.expires_on and self.expires_on < timezone.now()

        return version_is_valid and not expired
