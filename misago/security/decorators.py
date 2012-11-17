from misago.messages import Message
from misago.security.models import SignInAttempt
from misago.views import error403

def block_authenticated(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.user.is_authenticated():
            return error403(request, Message(request, 'security/forbidden_authenticated'))
        return f(*args, **kwargs)
    return decorator


def block_jammed(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.jam.is_jammed():
            return error403(request, Message(request, 'security/forbidden_jammed'))
        return f(*args, **kwargs)
    return decorator


def block_guest(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated():
            return error403(request, Message(request, 'security/forbidden_guest'))
        return f(*args, **kwargs)
    return decorator


def check_csrf(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.csrf.request_secure(request):
            return error403(request, Message(request, 'security/forbidden_request'))
        return f(*args, **kwargs)
    return decorator