from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.banning.models import check_ban
from misago.banning.decorators import block_banned
from misago.banning.views import error_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security import get_random_string
from misago.security.auth import sign_user_in
from misago.security.decorators import *
from misago.sessions.models import *
from misago.auth.forms import *
from misago.users.models import User, Group
from misago.views import error403, error404

@block_banned
@block_authenticated
@block_jammed
def register(request):
    if request.settings['account_activation'] == 'block':
        return error403(request, Message(request, 'auth/registrations_off'))
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
                                                Group.objects.get(pk=3), # Registered members
                                                ip=request.session.get_ip(request),
                                                activation=need_activation,
                                                request=request
                                                )
            if need_activation == User.ACTIVATION_NONE:
                # No need for activation, sign in user
                sign_user_in(request, new_user)
                request.messages.set_flash(Message(request, 'auth/registered_activation_none', extra={'user':new_user}), 'success')
            if need_activation == User.ACTIVATION_USER:
                # Mail user activation e-mail
                request.messages.set_flash(Message(request, 'auth/registered_activation_user', extra={'user':new_user}), 'info')
                new_user.email_user(
                                    request,
                                    'auth/activation_0',
                                    _("Welcome aboard, %(username)s!" % {'username': new_user.username}),
                                    )
            if need_activation == User.ACTIVATION_ADMIN:
                # Require admin activation
                request.messages.set_flash(Message(request, 'users/registered_activation_admin', extra={'user':new_user}), 'info')
            new_user.email_user(
                                request,
                                ('auth/activation_%s' % need_activation),
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
    return request.theme.render_to_response('auth/register.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                             'hide_signin': True, 
                                            },
                                            context_instance=RequestContext(request));


@block_banned
@block_authenticated
@block_jammed
def send_activation(request):
    message = None
    if request.method == 'POST':
        form = UserSendSpecialMailForm(request.POST, request=request)
        if form.is_valid():
            user = form.found_user
            user_ban = check_ban(username=user.username, email=user.email)
            if user_ban:
                return error_banned(request, user, user_ban)
            if user.activation == User.ACTIVATION_NONE:
                return error403(request, Message(request, 'auth/activation_not_required', extra={'user': user}))
            if user.activation == User.ACTIVATION_ADMIN:
                return error403(request, Message(request, 'auth/activation_only_by_admin', extra={'user': user}))
            request.messages.set_flash(Message(request, 'auth/activation_resent', extra={'user':user}), 'success')
            user.email_user(
                            request,
                            'auth/activation_resend',
                            _("New Account Activation"),
                            )
            return redirect(reverse('index'))
        else:
            message = Message(request, form.non_field_errors()[0])
    else:
        form = UserSendSpecialMailForm(request=request)
    return request.theme.render_to_response('auth/resend_activation.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                            },
                                            context_instance=RequestContext(request));
                                            
                                            
@block_banned
@block_authenticated
@block_jammed
def activate(request, username="", user="0", token=""):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        current_activation = user.activation
        # Run checks
        user_ban = check_ban(username=user.username, email=user.email)
        if user_ban:
            return error_banned(request, user, user_ban)
        if user.activation == User.ACTIVATION_NONE:
            return error403(request, Message(request, 'auth/activation_not_required', extra={'user': user}))
        if user.activation == User.ACTIVATION_ADMIN:
            return error403(request, Message(request, 'auth/activation_only_by_admin', extra={'user': user}))
        if not token or not user.token or user.token != token:
            return error403(request, Message(request, 'auth/invalid_confirmation_activation', extra={'user': user}))
        # Activate and sign in our member
        user.activation = User.ACTIVATION_NONE
        sign_user_in(request, user)
        if current_activation == User.ACTIVATION_PASSWORD:
            request.messages.set_flash(Message(request, 'auth/activated_password', extra={'user':user}), 'success')
        else:
            request.messages.set_flash(Message(request, 'auth/activated_new', extra={'user':user}), 'success')
        return redirect(reverse('index'))
    except User.DoesNotExist:
        return error404(request)


@block_banned
@block_authenticated
@block_jammed   
def forgot_password(request):
    message = None
    if request.method == 'POST':
        form = UserSendSpecialMailForm(request.POST, request=request)
        if form.is_valid():
            user = form.found_user
            user_ban = check_ban(username=user.username, email=user.email)
            if user_ban:
                return error_banned(request, user, user_ban)
            elif user.activation != User.ACTIVATION_NONE:
                return error403(request, Message(request, 'auth/activation_required', {'user': user}))
            user.token = get_random_string(12)
            user.save(force_update=True)
            request.messages.set_flash(Message(request, 'auth/password_reset_confirm', extra={'user':user}), 'success')
            user.email_user(
                            request,
                            'auth/reset_confirm',
                            _("Confirm New Password Request")
                            )
            return redirect(reverse('index'))
        else:
            message = Message(request, form.non_field_errors()[0])
    else:
        form = UserSendSpecialMailForm(request=request)
    return request.theme.render_to_response('auth/forgot_password.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                            },
                                            context_instance=RequestContext(request));


@block_banned
@block_authenticated
@block_jammed
def reset_password(request, username="", user="0", token=""):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        user_ban = check_ban(username=user.username, email=user.email)
        if user_ban:
            return error_banned(request, user, user_ban)
        if user.activation != User.ACTIVATION_NONE:
            return error403(request, Message(request, 'auth/activation_required', {'user': user}))
        if not token or not user.token or user.token != token:
            return error403(request, Message(request, 'auth/invalid_confirmation_link', {'user': user}))
        new_password = get_random_string(6)
        user.token = None
        user.set_password(new_password)
        user.save(force_update=True)
        # Logout signed in and kill remember me tokens
        Session.objects.filter(user=user).update(user=None)
        Token.objects.filter(user=user).delete()
        # Set flash and mail new password
        request.messages.set_flash(Message(request, 'auth/password_reset_done', extra={'user':user}), 'success')
        user.email_user(
                        request,
                        'auth/reset_new',
                        _("Your New Password"),
                        {'password': new_password}
                        )
        return redirect(reverse('sign_in'))
    except User.DoesNotExist:
        return error404(request)