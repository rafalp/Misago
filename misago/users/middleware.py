from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.messages import Message

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
            # Set user timezone and rank
            request.session.rank = request.user.rank_id
            set_timezone(request.user.timezone)
            
            # Display "welcome back!" message
            if request.session.remember_me:
                request.messages.set_message(Message(_("Welcome back, %(username)s! We've signed you in automatically for your convenience.") % {'username': request.user.username}), 'info')
        else:
            # Set guest's timezone and empty rank
            set_timezone(request.settings['default_timezone'])
            request.session.rank = None