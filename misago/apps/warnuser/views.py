from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago import messages
from misago.acl.exceptions import ACLError403
from misago.apps.errors import error403, error404
from misago.decorators import block_guest, check_csrf
from misago.models import User
from misago.shortcuts import render_to_response

@block_guest
@check_csrf
def warn_user(request, user, slug):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return error404(request, _("Requested user could not be found"))

    try:
        request.acl.warnings.allow_warning_members():
        user.acl().warnings.allow_warning()
    except ACLError403 as e:
        return error403(request, e)

    form = 123
    if ('origin' in request.POST
            and request.POST.get('origin') == 'warning_form'):
        pass
