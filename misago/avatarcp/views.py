from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.forms import FormLayout
from misago.messages import Message
from misago.usercp.template import RequestContext

@block_guest
def avatar(request):
    # Intercept all requests if we cant use avatar
    if request.user.avatar_ban:
        return request.theme.render_to_response('usercp/avatar_banned.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'avatar',
                                             }));
                                                   
    return request.theme.render_to_response('usercp/avatar.html',
                                            context_instance=RequestContext(request, {
                                              'tab': 'avatar',
                                             }));