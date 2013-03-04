from datetime import timedelta
from random import randint
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

"""
IP's that have exhausted their quota of sign-in attempts are automatically banned for set amount of time.

That IP ban cuts bad IP address from signing into board by either making another sign-in attempts or
registering "fresh" account.
"""
class SignInAttemptsManager(models.Manager):
    """
    Attempts manager
    """
    def register_attempt(self, ip):
        attempt = SignInAttempt(ip=ip, date=timezone.now())
        attempt.save(force_insert=True)

    def is_jammed(self, settings, ip):
        # Limit is off, dont jam IPs?
        if settings['attempts_limit'] == 0:
            return False
        # Check jam
        if settings['jams_lifetime'] > 0:
            attempts = SignInAttempt.objects.filter(
                                                    date__gt=timezone.now() - timedelta(minutes=settings['jams_lifetime']),
                                                    ip=ip
                                                    )
        else:
            attempts = SignInAttempt.objects.filter(ip=ip)
        return attempts.count() > settings['attempts_limit']


class SignInAttempt(models.Model):
    ip = models.GenericIPAddressField()
    date = models.DateTimeField()

    objects = SignInAttemptsManager()


class JamCache(object):
    jammed = False
    expires = timezone.now()
    def check_for_updates(self, request):
        if self.expires < timezone.now():
            self.jammed = SignInAttempt.objects.is_jammed(request.settings, request.session.get_ip(request))
            self.expires = timezone.now() + timedelta(minutes=request.settings['jams_lifetime'])
            return True
        return False

    def is_jammed(self):
        return self.jammed
