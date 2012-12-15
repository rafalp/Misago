from misago.authn.decorators import block_guest
from misago.usercp.template import RequestContext

@block_guest
def blocked(request):
    return request.theme.render_to_response('usercp/blocked.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'blocked',
                                             }));