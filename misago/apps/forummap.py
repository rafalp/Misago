from django.template import RequestContext
from misago.models import Forum

def forum_map(request):
    return request.theme.render_to_response('forum_map.html',
                                            {
                                             'forums': Forum.objects.treelist(request.acl.forums),
                                             },
                                            context_instance=RequestContext(request));