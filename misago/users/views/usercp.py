from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.forms import FormLayout
from misago.security.decorators import *
from misago.users.forms import UserForumOptionsForm


@block_guest   
def options(request):
    form = UserForumOptionsForm(request=request,initial={
                                                         'timezone': request.user.timezone
                                                         })
    
    return request.theme.render_to_response('users/usercp/options.html',
                                            {
                                             'tab': 'options',
                                             'form': FormLayout(form)
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def credentials(request):
    return request.theme.render_to_response('users/usercp/credentials.html',
                                            {
                                             'tab': 'credentials',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def username(request):
    return request.theme.render_to_response('users/usercp/username.html',
                                            {
                                             'tab': 'username',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def avatar(request):
    # Intercept all requests if we cant use avatar
    if request.user.avatar_ban:
        return request.theme.render_to_response('users/usercp/avatar_banned.html',
                                                {'tab': 'avatar'},
                                                context_instance=RequestContext(request));
                                                   
    return request.theme.render_to_response('users/usercp/avatar.html',
                                            {
                                             'tab': 'avatar',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def signature(request):
    # Intercept all requests if we cant use signature
    if request.user.avatar_ban:
        return request.theme.render_to_response('users/usercp/signature_banned.html',
                                                {'tab': 'signature'},
                                                context_instance=RequestContext(request));
                                                
    return request.theme.render_to_response('users/usercp/signature.html',
                                            {
                                             'tab': 'signature',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def ignored(request):
    return request.theme.render_to_response('users/usercp/ignored.html',
                                            {
                                             'tab': 'ignored',
                                             },
                                            context_instance=RequestContext(request));