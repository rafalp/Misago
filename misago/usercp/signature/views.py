from misago.authn.decorators import block_guest
from misago.usercp.template import RequestContext

@block_guest
def signature(request):
    # Intercept all requests if we cant use signature
    if request.user.signature_ban:
        return request.theme.render_to_response('usercp/signature_banned.html',
                                                context_instance=RequestContext(request, {
                                                  'tab': 'signature',
                                                 }));
                                                
    return request.theme.render_to_response('usercp/signature.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'signature',
                                             }));