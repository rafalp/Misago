from django.utils.translation import ugettext as _
from misago.views import error403

def block_authenticated(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.user.is_authenticated():
            return error403(request, _("%{username}s, this page is not available to signed in users.") % {'username': request.user.username})
        return f(*args, **kwargs)
    return decorator


def block_guest(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return error403(request, _("Dear Guest, only signed in members are allowed to access this page. Please sign in or register and try again."))
        return f(*args, **kwargs)
    return decorator