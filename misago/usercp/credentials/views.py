from misago.authn.decorators import block_guest
from misago.usercp.template import RequestContext

@block_guest
def credentials(request):
    return request.theme.render_to_response('usercp/credentials.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'credentials',
                                             }));