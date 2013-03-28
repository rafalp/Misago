from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.decorators import block_guest
from misago.forms import FormLayout
from misago.messages import Message
from misago.apps.usercp.options.forms import UserForumOptionsForm
from misago.apps.usercp.template import RequestContext

@block_guest
def options(request):
    message = request.messages.get_message('usercp_options')
    if request.method == 'POST':
        form = UserForumOptionsForm(request.POST, request=request)
        if form.is_valid():
            request.user.hide_activity = form.cleaned_data['hide_activity']
            request.user.allow_pds = form.cleaned_data['allow_pds']
            request.user.receive_newsletters = form.cleaned_data['newsletters']
            request.user.timezone = form.cleaned_data['timezone']
            request.user.subscribe_start = form.cleaned_data['subscribe_start']
            request.user.subscribe_reply = form.cleaned_data['subscribe_reply']
            request.user.save(force_update=True)
            request.messages.set_flash(Message(_("Forum options have been changed.")), 'success', 'usercp_options')
            return redirect(reverse('usercp'))
        message = Message(form.non_field_errors()[0], 'error')
    else:
        form = UserForumOptionsForm(request=request, initial={
                                                             'newsletters': request.user.receive_newsletters,
                                                             'hide_activity': request.user.hide_activity,
                                                             'allow_pds': request.user.allow_pds,
                                                             'timezone': request.user.timezone,
                                                             'subscribe_start': request.user.subscribe_start,
                                                             'subscribe_reply': request.user.subscribe_reply,
                                                             })

    return request.theme.render_to_response('usercp/options.html',
                                            context_instance=RequestContext(request, {
                                             'message': message,
                                             'tab': 'options',
                                             'form': FormLayout(form)
                                             }));
