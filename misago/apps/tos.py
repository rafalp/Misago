from django.template import RequestContext
from misago.apps.errors import error404
from misago.conf import settings
from misago.shortcuts import render_to_response

def tos(request):
    if settings.tos_url or not settings.tos_content:
        return error404(request)
    return render_to_response('forum_tos.html',
                              context_instance=RequestContext(request));
