from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from misago.users.decorators import deflect_authenticated, deflect_banned_ips


@sensitive_post_parameters()
@deflect_authenticated
@deflect_banned_ips
def activation_noscript(request, user_id=None, token=None):
    return noscript(request, **{
        'title': _("Activate your account"),
        'message': _("To activate your account enable JavaScript."),
    })
