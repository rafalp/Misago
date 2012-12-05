from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.forms import FormLayout
from misago.messages import Message
from misago.auth.decorators import block_guest
from misago.usercp.forms import UserForumOptionsForm


@block_guest   
def options(request):
    message = request.messages.get_message('usercp_options')
    if request.method == 'POST':
        form = UserForumOptionsForm(request.POST, request=request)
        if form.is_valid():
            request.user.receive_newsletters = form.cleaned_data['newsletters']
            request.user.hide_activity = form.cleaned_data['hide_activity']
            request.user.timezone = form.cleaned_data['timezone']
            request.user.save(force_update=True)
            request.messages.set_flash(Message(_("Forum options have been changed.")), 'success', 'usercp_options')
            return redirect(reverse('usercp'))
        message = Message(form.non_field_errors()[0], 'error')
    else:
        form = UserForumOptionsForm(request=request,initial={
                                                             'newsletters': request.user.receive_newsletters,
                                                             'hide_activity': request.user.hide_activity,
                                                             'timezone': request.user.timezone,
                                                             })
    
    return request.theme.render_to_response('usercp/options.html',
                                            {
                                             'message': message,
                                             'tab': 'options',
                                             'form': FormLayout(form)
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def credentials(request):
    return request.theme.render_to_response('usercp/credentials.html',
                                            {
                                             'tab': 'credentials',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def username(request):
    return request.theme.render_to_response('usercp/username.html',
                                            {
                                             'tab': 'username',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def avatar(request):
    # Intercept all requests if we cant use avatar
    if request.user.avatar_ban:
        return request.theme.render_to_response('usercp/avatar_banned.html',
                                                {'tab': 'avatar'},
                                                context_instance=RequestContext(request));
                                                   
    return request.theme.render_to_response('usercp/avatar.html',
                                            {
                                             'tab': 'avatar',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def signature(request):
    # Intercept all requests if we cant use signature
    if request.user.avatar_ban:
        return request.theme.render_to_response('usercp/signature_banned.html',
                                                {'tab': 'signature'},
                                                context_instance=RequestContext(request));
                                                
    return request.theme.render_to_response('usercp/signature.html',
                                            {
                                             'tab': 'signature',
                                             },
                                            context_instance=RequestContext(request));
    
 
@block_guest
def ignored(request):
    return request.theme.render_to_response('usercp/ignored.html',
                                            {
                                             'tab': 'ignored',
                                             },
                                            context_instance=RequestContext(request));