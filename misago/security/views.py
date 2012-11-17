from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.banning.decorators import block_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security import get_random_string
import misago.security.auth as auth
from misago.security.auth import AuthException, auth_admin, auth_forum, sign_user_in
from misago.security.decorators import *
from misago.security.models import SignInAttempt
from misago.sessions.models import Token
from forms import SignInForm

@block_banned
@block_authenticated
@block_jammed
def signin(request):
    message = request.messages.get_message('security')
    if request.method == 'POST':
        form = SignInForm(
                          request.POST,
                          show_remember_me=not request.firewall.admin and request.settings['remember_me_allow'],
                          show_stay_hidden=not request.firewall.admin and request.settings['sessions_hidden'],
                          request=request
                          )
        if form.is_valid():
            try:
                # Configure correct auth and redirect links
                if request.firewall.admin:
                    auth_method = auth_admin
                    success_redirect = reverse(site.get_admin_index())
                else:
                    auth_method = auth_forum
                    success_redirect = reverse('index')
                
                # Authenticate user
                user = auth_method(
                                  request,
                                  form.cleaned_data['user_email'],
                                  form.cleaned_data['user_password'],
                                  )
                
                if not request.firewall.admin and request.settings['sessions_hidden'] and form.cleaned_data['user_stay_hidden']:
                    request.session.hidden = True                    
                
                sign_user_in(request, user, request.session.hidden)     
                           
                remember_me_token = False
                if not request.firewall.admin and request.settings['remember_me_allow'] and form.cleaned_data['user_remember_me']:
                    remember_me_token = get_random_string(42)
                    remember_me = Token(
                                        id=remember_me_token,
                                        user=user,
                                        created=timezone.now(),
                                        accessed=timezone.now(),
                                        hidden=request.session.hidden
                                        )
                    remember_me.save()
                if remember_me_token:
                    request.cookie_jar.set('TOKEN', remember_me_token, True)
                request.messages.set_flash(Message(request, 'security/signed_in', extra={'user': user}), 'success', 'security')
                return redirect(success_redirect)
            except AuthException as e:
                message = Message(request, e.type, extra={'user':e.user})
                message.type = 'error'
                # If not in Admin, register failed attempt
                if not request.firewall.admin and e.type == auth.CREDENTIALS:
                    SignInAttempt.objects.register_attempt(request.session.get_ip(request))
                    # Have we jammed our account?
                    if SignInAttempt.objects.is_jammed(request.settings, request.session.get_ip(request)):
                        request.jam.expires = timezone.now()
                        return redirect(reverse('sign_in'))
        else:
            message = Message(request, form.non_field_errors()[0])
            message.type = 'error'
    else:
        form = SignInForm(
                          show_remember_me=not request.firewall.admin and request.settings['remember_me_allow'],
                          show_stay_hidden=not request.firewall.admin and request.settings['sessions_hidden'],
                          request=request
                          )
    return request.theme.render_to_response('signin.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form, [
                                                 (
                                                     None,
                                                     [('user_email', {'attrs': {'placeholder': _("Enter your e-mail")}}), ('user_password', {'has_value': False, 'placeholder': _("Enter your password")})]
                                                 ),
                                                 (
                                                     None,
                                                     ['user_remember_me', 'user_stay_hidden'],
                                                 ),
                                             ]),
                                             'hide_signin': True, 
                                            },
                                            context_instance=RequestContext(request));


@block_guest
@check_csrf
def signout(request):
    user = request.user
    request.session.sign_out(request)
    request.messages.set_flash(Message(request, 'security/signed_out', extra={'user': user}), 'info', 'security')
    if request.firewall.admin:
        return redirect(reverse(site.get_admin_index()))
    return redirect(reverse('index'))
    