from django.utils.translation import ugettext as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404, error_banned

def acl_errors(f):
    def decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ACLError403 as e:
            return error403(args[0], e)
        except ACLError404 as e:
            return error404(args[0], e)
    return decorator


def block_authenticated(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.user.is_authenticated():
            return error403(request, _("%(username)s, this page is not available to signed in users.") % {'username': request.user.username})
        return f(*args, **kwargs)
    return decorator


def block_banned(f):
    def decorator(*args, **kwargs):
        request = args[0]
        try:
            if request.ban.is_banned():
                return error_banned(request);
            return f(*args, **kwargs)
        except AttributeError:
            pass
        return f(*args, **kwargs)
    return decorator


def block_crawlers(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if request.user.is_crawler():
            return error403(request)
        return f(*args, **kwargs)
    return decorator


def block_guest(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return error403(request, _("Dear Guest, only signed in members are allowed to access this page. Please sign in or register and try again."))
        return f(*args, **kwargs)
    return decorator


def block_jammed(f):
    def decorator(*args, **kwargs):
        request = args[0]
        try:
            if not request.firewall.admin and request.jam.is_jammed():
                return error403(request, _("You have used up allowed attempts quota and we temporarily banned you from accessing this page."))
        except AttributeError:
            pass
        return f(*args, **kwargs)
    return decorator


def check_csrf(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.csrf.request_secure(request):
            return error403(request, _("Request authorization is invalid. Please try again."))
        return f(*args, **kwargs)
    return decorator