from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
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
        request.onlines = MembersOnline(request.monitor, request.settings['sessions_tracker_sync_frequency'])

        if request.session.created() and not request.firewall.admin:
            request.onlines.new_session()

        if request.user.is_authenticated():
            # Set user timezone and rank
            request.session.rank = request.user.rank_id
            set_timezone(request.user.timezone)

            # Display "welcome back!" message
            if request.session.remember_me:
                request.onlines.sign_in()
                request.messages.set_message(Message(_("Welcome back, %(username)s! We've signed you in automatically for your convenience.") % {'username': request.user.username}), 'info')
        else:
            # Set guest's timezone and empty rank
            set_timezone(request.settings['default_timezone'])
            request.session.rank = None

    def process_response(self, request, response):
        try:
            request.onlines.sync()
        except AttributeError:
            pass
        return response
