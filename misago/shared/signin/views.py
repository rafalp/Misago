from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.forms import FormLayout
from misago.messages import Message
import misago.auth as auth
from misago.auth.decorators import 
from misago.shared.signin.forms import SignInForm
from misago.auth import AuthException, auth_admin, auth_forum, sign_user_in
from misago.decorators import (block_authenticated, block_banned, block_crawlers,
                            block_guest, block_jammed, check_csrf)
from misago.models import SignInAttempt, Token
from misago.utils import random_string

@block_crawlers
@block_banned
@block_authenticated
@block_jammed
def signin(request):
    message = request.messages.get_message('security')
    bad_password = False
    not_active = False
    banned_account = False

    if request.method == 'POST':
        form = SignInForm(
                          request.POST,
                          show_remember_me=not request.firewall.admin and request.settings['remember_me_allow'],
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

                sign_user_in(request, user)
                remember_me_token = False

                if not request.firewall.admin and request.settings['remember_me_allow'] and form.cleaned_data['user_remember_me']:
                    remember_me_token = random_string(42)
                    remember_me = Token(
                                        id=remember_me_token,
                                        user=user,
                                        created=timezone.now(),
                                        accessed=timezone.now(),
                                        )
                    remember_me.save()
                if remember_me_token:
                    request.cookie_jar.set('TOKEN', remember_me_token, True)
                request.messages.set_flash(Message(_("Welcome back, %(username)s!") % {'username': user.username}), 'success', 'security')
                return redirect(success_redirect)
            except AuthException as e:
                message = Message(e.error, 'error')
                bad_password = e.password
                banned_account = e.ban
                not_active = e.activation

                # If not in Admin, register failed attempt
                if not request.firewall.admin and e.type == auth.CREDENTIALS:
                    SignInAttempt.objects.register_attempt(request.session.get_ip(request))

                    # Have we jammed our account?
                    if SignInAttempt.objects.is_jammed(request.settings, request.session.get_ip(request)):
                        request.jam.expires = timezone.now()
                        return redirect(reverse('sign_in'))
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = SignInForm(
                          show_remember_me=not request.firewall.admin and request.settings['remember_me_allow'],
                          request=request
                          )
    return request.theme.render_to_response('signin.html',
                                            {
                                             'message': message,
                                             'bad_password': bad_password,
                                             'banned_account': banned_account,
                                             'not_active': not_active,
                                             'form': FormLayout(form),
                                             'hide_signin': True,
                                             },
                                            context_instance=RequestContext(request));


@block_crawlers
@block_guest
@check_csrf
def signout(request):
    user = request.user
    request.session.sign_out(request)
    request.messages.set_flash(Message(_("You have been signed out.")), 'info', 'security')
    if request.firewall.admin:
        return redirect(reverse(site.get_admin_index()))
    return redirect(reverse('index'))
