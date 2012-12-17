from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.sessions.models import Session
from misago.forums.models import Forum

def home(request):
    team_online = []
    team_pks = []
    for session in Session.objects.filter(team=1).filter(admin=0).order_by('-start').select_related('user', 'user__rank'):
        if session.user.pk not in team_pks:
            team_pks.append(session.user.pk)
            team_online.append(session.user)
            
    return request.theme.render_to_response('index.html',
                                        {
                                         'forums_list': Forum.objects.treelist(request.acl.forums.known_forums()),
                                         'team_online': team_online,
                                         },
                                        context_instance=RequestContext(request));


def redirect_message(request, message, type='info', owner=None):
    request.messages.set_flash(message, type, owner)
    return redirect(reverse('index'))


def error403(request, message=None):
    return error_view(request, 403, message)

                                            
def error404(request, message=None):
    return error_view(request, 404, message)


def error_view(request, error, message):
    response = request.theme.render_to_response(('error%s.html' % error),
                                            {
                                             'message': message,
                                             'hide_signin': True,
                                             'exception_response': True,
                                             },
                                            context_instance=RequestContext(request));
    response.status_code = error
    return response