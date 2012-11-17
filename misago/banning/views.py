from django.utils.translation import ugettext as _
from misago.messages import Message
from misago.views import error403

def error_banned(request, user=False):
    if not user:
        user = request.user
    if user.is_banned():
        return error403(request, Message(request, 'banning/banned_user', extra={'user': user}), _("You are banned"));
    if request.ban.is_banned():
        return error403(request, Message(request, 'banning/banned_ip'), _("You are banned"));