from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.core.views import noscript

from misago.users.bans import get_user_ban
from misago.users.decorators import deflect_authenticated, deflect_banned_ips


@sensitive_post_parameters()
@deflect_authenticated
@deflect_banned_ips
def forgotten_password_noscript(request, user_id=None, token=None):
    return noscript(request, **{
        'title': _("Change forgotten password"),
        'message': _("To change forgotten password enable JavaScript."),
    })
