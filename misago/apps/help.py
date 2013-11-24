from django.template import RequestContext
from misago.shortcuts import render_to_response

def markdown(request):
    return render_to_response('help_md.html',
                              context_instance=RequestContext(request));