from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.usercp.template import RequestContext
 
@block_guest
def credentials(request):
    return request.theme.render_to_response('usercp/credentials.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'credentials',
                                             }));
    
 
@block_guest
def username(request):
    return request.theme.render_to_response('usercp/username.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'username',
                                             }));  
 
@block_guest
def signature(request):
    # Intercept all requests if we cant use signature
    if request.user.avatar_ban:
        return request.theme.render_to_response('usercp/signature_banned.html',
                                                context_instance=RequestContext(request, {
                                                  'tab': 'signature',
                                                 }));
                                                
    return request.theme.render_to_response('usercp/signature.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'signature',
                                             }));
    
 
@block_guest
def ignored(request):
    return request.theme.render_to_response('usercp/ignored.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'ignored',
                                             }));