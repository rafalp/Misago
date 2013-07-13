from datetime import timedelta
from django.utils import timezone
from misago.conf import settings
from misago.models import SignInAttempt

class JamCache(object):
    def __init__(self):
        self.jammed = False
        self.expires = timezone.now()
    
    def check_for_updates(self, request):
        if self.expires < timezone.now():
            self.jammed = SignInAttempt.objects.is_jammed(request.session.get_ip(request))
            self.expires = timezone.now() + timedelta(minutes=settings.jams_lifetime)
            return True
        return False

    def is_jammed(self):
        return self.jammed


class JamMiddleware(object):
    def process_request(self, request):
        if request.user.is_crawler():
            return None
        try:
            request.jam = request.session['jam']
        except KeyError:
            request.jam = JamCache()
            request.session['jam'] = request.jam
        if not request.firewall.admin:
            request.jam.check_for_updates(request)
