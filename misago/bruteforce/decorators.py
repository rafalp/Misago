from django.utils.translation import ugettext as _
from misago.views import error403

def block_jammed(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if not request.firewall.admin and request.jam.is_jammed():
            return error403(request, _("You have used up allowed attempts quota and we temporarily banned you from accessing this page."))
        return f(*args, **kwargs)
    return decorator