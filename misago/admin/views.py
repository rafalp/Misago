from django.template import RequestContext
from misago.sessions.models import Session

def home(request):
    return request.theme.render_to_response('home.html', {
        'users': request.monitor['users'],
        'users_inactive': request.monitor['users_inactive'],
        'threads': request.monitor['threads'],
        'posts': request.monitor['posts'],
        'admins': Session.objects.filter(user__isnull=False).filter(admin=1).order_by('user__username_slug').select_related(depth=1),
        }, context_instance=RequestContext(request));


def todo(request):
    return request.theme.render_to_response('todo.html', context_instance=RequestContext(request));
