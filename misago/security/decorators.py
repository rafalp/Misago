from django.utils.translation import ugettext_lazy as _
from misago.security.models import SignInAttempt
from misago.views import error403

def block_authenticated(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.user.is_authenticated():
            return error403(request, _("%{username}s, this page is not available to signed in users.") % {'username': request.user.username})
        return f(*args, **kwargs)
    return decorator


def block_jammed(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.jam.is_jammed():
            return error403(request, _("You have used up allowed sign-in attempts quota and we temporarily banned you from signing in."))
        return f(*args, **kwargs)
    return decorator


def block_guest(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return error403(request, _("Dear Guest, only signed in members are allowed to access this page. Please sign in or register and try again."))
        return f(*args, **kwargs)
    return decorator


def check_csrf(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.csrf.request_secure(request):
            return error403(request, _("Request authorization is invalid. Please try again."))
        return f(*args, **kwargs)
    return decorator