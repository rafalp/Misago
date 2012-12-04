from django.template import RequestContext
from misago.messages import Message

def error_banned(request, user=None, ban=None):
    if not ban:
        ban = request.ban
    response = request.theme.render_to_response('error403_banned.html',
                                                {
                                                 'banned_user': user,
                                                 'ban': ban,
                                                 'hide_signin': True,
                                                 'exception_response': True,
                                                 },
                                                context_instance=RequestContext(request));
    response.status_code = 403
    return response