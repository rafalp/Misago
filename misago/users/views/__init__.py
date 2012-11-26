from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.banning.decorators import block_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security.auth import sign_user_in
from misago.security.decorators import *
from misago.users.forms import *
from misago.users.models import User
from misago.views import error403

@block_banned
@block_authenticated
@block_jammed
def register(request):
    if request.settings['account_activation'] == 'block':
        return error403(request, Message(request, 'users/registration/registrations_off'))
    message = None
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request=request)
        if form.is_valid():
            need_activation = 0
            if request.settings['account_activation'] == 'user':
                need_activation = User.ACTIVATION_USER
            if request.settings['account_activation'] == 'admin':
                need_activation = User.ACTIVATION_ADMIN
                
            new_user = User.objects.create_user(
                                                form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['password'],
                                                ip=request.session.get_ip(request),
                                                activation=need_activation,
                                                request=request
                                                )
                        
            if need_activation == User.ACTIVATION_NONE:
                # No need for activation, sign in user
                sign_user_in(request, new_user)
                request.messages.set_flash(Message(request, 'users/activation/none', extra={'user':new_user}), 'success')
            if need_activation == User.ACTIVATION_USER:
                # Mail user activation e-mail
                request.messages.set_flash(Message(request, 'users/registration/activation_user', extra={'user':new_user}), 'info')
                new_user.email_user(
                                    request,
                                    'users/activation/user',
                                    _("Welcome aboard, %(username)s!" % {'username': new_user.username}),
                                    )
            if need_activation == User.ACTIVATION_ADMIN:
                # Require admin activation
                request.messages.set_flash(Message(request, 'users/registration/activation_admin', extra={'user':new_user}), 'info')
            new_user.email_user(
                                request,
                                'users/activation/admin',
                                _("Welcome aboard, %(username)s!" % {'username': new_user.username}),
                                {'password': form.cleaned_data['password']}
                                )
            return redirect(reverse('index'))
        else:
            message = Message(request, form.non_field_errors()[0])
            if request.settings['registrations_jams']:
                SignInAttempt.objects.register_attempt(request.session.get_ip(request))
            # Have we jammed our account?
            if SignInAttempt.objects.is_jammed(request.session.get_ip(request)):
                request.jam.expires = timezone.now()
                return redirect(reverse('register'))
    else:
        form = UserRegisterForm(request=request)
    return request.theme.render_to_response('users/register.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                             'hide_signin': True, 
                                            },
                                            context_instance=RequestContext(request));