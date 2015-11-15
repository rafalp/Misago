from django.utils.translation import ugettext as _
from misago.users.decorators import deny_authenticated, deny_banned_ips


@deny_authenticated
@deny_banned_ips
def forgotten_password_noscript(request, user_id=None, token=None):
    return noscript(request, **{
        'title': _("Change forgotten password"),
        'message': _("To change forgotten password enable JavaScript."),
    })
