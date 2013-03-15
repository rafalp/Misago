from django.utils.translation import ugettext as _

def check_csrf(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.csrf.request_secure(request):
            from misago.views import error403
            return error403(request, _("Request authorization is invalid. Please try again."))
        return f(*args, **kwargs)
    return decorator
