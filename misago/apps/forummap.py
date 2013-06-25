from django.template import RequestContext
from misago.models import Forum
from misago.shortcuts import render_to_response

def forum_map(request):
    return render_to_response('forum_map.html',
                              {'forums': Forum.objects.treelist(request.acl.forums),},
                              context_instance=RequestContext(request));