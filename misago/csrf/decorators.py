from django.utils.translation import ugettext as _
from misago.views import error403

def check_csrf(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.csrf.request_secure(request):
            return error403(request, _("Request authorization is invalid. Please try again."))
        return f(*args, **kwargs)
    return decorator