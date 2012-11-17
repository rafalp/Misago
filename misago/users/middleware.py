from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
            # Set user timezone
            set_timezone(request.user.timezone)
            
            # Display "welcome back!" message
            if request.session.remember_me:
                request.messages.set_message(_("We have signed you in automatically."), 'info', _("Welcome back, %(username)s!" % {'username': request.user.username}))
        else:
            # Set guest's timezone
            set_timezone(request.settings['default_timezone'])