from django.utils.translation import ugettext as _
from misago.messages import Message
from misago.views import error403

def error_banned(request, user=None, ban=None):
    if not user:
        user = request.user
    if not ban:
        ban = request.ban
    return error403(request, Message(request, 'banned', extra={'user': user, 'ban': ban}), _("You are banned"));