from django.template import RequestContext

def todo(request):
    return request.theme.render_to_response('todo.html', context_instance=RequestContext(request));