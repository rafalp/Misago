from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.conf import settings
from misago.messages import Message
from misago.onlines import MembersOnline

def set_timezone(new_tz):
    if settings.USE_TZ:
        try:
            import pytz
            timezone.activate(pytz.timezone(new_tz))
        except ImportError:
            pass


class UserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.session.rank = request.user.rank_id
            set_timezone(request.user.timezone)
            if request.session.remember_me:
                request.messages.set_message(Message(_("Welcome back, %(username)s! We've signed you in automatically for your convenience.") % {'username': request.user.username}), 'info')
        else:
            set_timezone(settings.default_timezone)
            request.session.rank = None
        request.onlines = MembersOnline(settings.online_counting, request.monitor, settings.online_counting_frequency)

    def process_response(self, request, response):
        try:
            request.onlines.sync()
        except AttributeError:
            pass
        return response
