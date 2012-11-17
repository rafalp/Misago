from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from misago.security.decorators import *
from misago.users.models import User, Group
from misago.views import error403, error404


def users(request):
    pass


def user_profile(request, user, username):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        if user.username_slug != username:
            # Force crawlers to take notice of updated username
            return redirect(reverse('user', args=(user.username_slug, user.pk)), permanent=True)
        return request.theme.render_to_response('users/profile.html',
                                            {
                                             'profile': user,
                                            },
                                            context_instance=RequestContext(request));
    except User.DoesNotExist:
        return error404(request)


@block_guest   
def usercp_options(request):
    return request.theme.render_to_response('users/usercp/options.html',
                                            {
                                             'tab': 'options',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def usercp_credentials(request):
    return request.theme.render_to_response('users/usercp/credentials.html',
                                            {
                                             'tab': 'credentials',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def usercp_username(request):
    return request.theme.render_to_response('users/usercp/username.html',
                                            {
                                             'tab': 'username',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def usercp_avatar(request):
    return request.theme.render_to_response('users/usercp/avatar.html',
                                            {
                                             'tab': 'avatar',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def usercp_signature(request):
    return request.theme.render_to_response('users/usercp/signature.html',
                                            {
                                             'tab': 'signature',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def usercp_ignored(request):
    return request.theme.render_to_response('users/usercp/ignored.html',
                                            {
                                             'tab': 'ignored',
                                             },
                                            context_instance=RequestContext(request));