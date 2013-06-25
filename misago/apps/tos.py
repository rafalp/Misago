from django.template import RequestContext
from misago.shortcuts import render_to_response
from misago.apps.errors import error404

def tos(request):
    if request.settings.tos_url or not request.settings.tos_content:
        return error404(request)
    return render_to_response('forum_tos.html',
                              context_instance=RequestContext(request));
