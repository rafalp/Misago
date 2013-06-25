from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.apps.errors import error403, error404
from misago.decorators import block_guest
from misago.forms import FormLayout
from misago.markdown import signature_markdown
from misago.messages import Message
from misago.shortcuts import render_to_response
from misago.apps.usercp.template import RequestContext
from misago.apps.usercp.signature.forms import SignatureForm

@block_guest
def signature(request):
    # Intercept all requests if we can't use signature
    if not request.acl.usercp.can_use_signature():
        return error403(request)
    if request.user.signature_ban:
        return render_to_response('usercp/signature_banned.html',
                                  context_instance=RequestContext(request, {
                                      'tab': 'signature'}));

    siggy_text = ''
    message = request.messages.get_message('usercp_signature')
    if request.method == 'POST':
        form = SignatureForm(request.POST, request=request, initial={'signature': request.user.signature})
        if form.is_valid():
            request.user.signature = form.cleaned_data['signature']
            if request.user.signature:
                request.user.signature_preparsed = signature_markdown(request.acl,
                                                                      request.user.signature)
            else:
                request.user.signature_preparsed = None
            request.user.save(force_update=True)
            request.messages.set_flash(Message(_("Your signature has been changed.")), 'success', 'usercp_signature')
            return redirect(reverse('usercp_signature'))
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = SignatureForm(request=request, initial={'signature': request.user.signature})

    return render_to_response('usercp/signature.html',
                              context_instance=RequestContext(request, {
                                  'message': message,
                                  'tab': 'signature',
                                  'form': FormLayout(form)}));
