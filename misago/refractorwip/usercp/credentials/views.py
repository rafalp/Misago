from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.forms import FormLayout
from misago.messages import Message
from misago.usercp.template import RequestContext
from misago.usercp.credentials.forms import CredentialsChangeForm
from misago.views import error404
from misago.utils import get_random_string

@block_guest
def credentials(request):
    message = request.messages.get_message('usercp_credentials')
    if request.method == 'POST':
        form = CredentialsChangeForm(request.POST, request=request)
        if form.is_valid():
            token = get_random_string(12)
            request.user.email_user(
                                    request,
                                    'users/new_credentials',
                                    _("Activate new Sign-In Credentials"),
                                    {'token': token}
                                    )
            request.session['new_credentials'] = {
                                                  'token': token,
                                                  'email_hash': request.user.email_hash,
                                                  'new_email': form.cleaned_data['new_email'],
                                                  'new_password': form.cleaned_data['new_password'],
                                                  }
            if form.cleaned_data['new_email']:
                request.user.email = form.cleaned_data['new_email']
                request.messages.set_flash(Message(_("We have sent e-mail message to your new e-mail address with link you have to click to confirm change of your sign-in credentials. This link will be valid only for duration of this session, do not sign out until you confirm change!")), 'success', 'usercp_credentials')
            else:
                request.messages.set_flash(Message(_("We have sent e-mail message to your e-mail address with link you have to click to confirm change of your sign-in credentials. This link will be valid only for duration of this session, do not sign out until you confirm change!")), 'success', 'usercp_credentials')
            return redirect(reverse('usercp_credentials'))
        message = Message(form.non_field_errors()[0], 'error')
    else:
        form = CredentialsChangeForm(request=request)

    return request.theme.render_to_response('usercp/credentials.html',
                                            context_instance=RequestContext(request, {
                                             'message': message,
                                             'form': FormLayout(form),
                                             'tab': 'credentials',
                                             }));


@block_guest
def activate(request, token):
    new_credentials = request.session.get('new_credentials')
    if not new_credentials or new_credentials['token'] != token:
        return error404(request)

    if new_credentials['new_email']:
        request.user.set_email(new_credentials['new_email'])
    if new_credentials['new_password']:
        request.user.set_password(new_credentials['new_password'])

    try:
        request.user.full_clean()
        request.user.save(force_update=True)
        request.user.sessions.exclude(id=request.session.id).delete()
        request.user.signin_tokens.all().delete()
        request.messages.set_flash(Message(_("%(username)s, your Sign-In credentials have been changed.") % {'username': request.user.username}), 'success', 'security')
        request.session.sign_out(request)
        del request.session['new_credentials']
        return redirect(reverse('sign_in'))
    except ValidationError:
        request.messages.set_flash(Message(_("Your new credentials have been invalidated. Please try again.")), 'error', 'usercp_credentials')
        return redirect(reverse('usercp_credentials'))
