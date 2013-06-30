from django.template import RequestContext
from misago.models import Session
from misago.monitor import monitor
from misago.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html',
                              {
                               'users': monitor.users,
                               'users_inactive': monitor.users_inactive,
                               'threads': monitor.threads,
                               'posts': monitor.posts,
                               'admins': Session.objects.filter(user__isnull=False).filter(admin=1).order_by('user__username_slug').select_related('user'),
                              },
                              context_instance=RequestContext(request));


def todo(request, *args, **kwargs):
    return render_to_response('todo.html', context_instance=RequestContext(request));
