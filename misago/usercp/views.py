from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.forms import FormLayout
from misago.messages import Message
from misago.authn.decorators import block_guest
from misago.usercp.forms import UserForumOptionsForm
from misago.usercp.template import RequestContext


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
                                            context_instance=RequestContext(request, {
                                              'message': message,
                                              'tab': 'options',
                                              'form': FormLayout(form)
                                             }));
    
 
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