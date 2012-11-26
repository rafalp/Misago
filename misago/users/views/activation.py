from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.banning.models import check_ban
from misago.banning.decorators import block_banned
from misago.banning.views import error_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security.auth import sign_user_in
from misago.security.decorators import *
from misago.users.forms import *
from misago.users.models import User
from misago.views import error403, error404


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
            return error403(request, Message(request, 'users/activation/not_required', extra={'user': user}))
        if user.activation == User.ACTIVATION_ADMIN:
            return error403(request, Message(request, 'users/activation/only_by_admin', extra={'user': user}))
        if not token or not user.token or user.token != token:
            return error403(request, Message(request, 'users/invalid_confirmation_link', extra={'user': user}))
        
        # Activate and sign in our member
        user.activation = User.ACTIVATION_NONE
        sign_user_in(request, user)
        
        # Update monitor
        request.monitor['users_inactive'] = request.monitor['users_inactive'] - 1
        
        if current_activation == User.ACTIVATION_CREDENTIALS:
            request.messages.set_flash(Message(request, 'users/activation/credentials', extra={'user':user}), 'success')
        else:
            request.messages.set_flash(Message(request, 'users/activation/new', extra={'user':user}), 'success')
        return redirect(reverse('index'))
    except User.DoesNotExist:
        return error404(request)


@block_banned
@block_authenticated
@block_jammed
def form(request):
    message = None
    if request.method == 'POST':
        form = UserSendSpecialMailForm(request.POST, request=request)
        if form.is_valid():
            user = form.found_user
            user_ban = check_ban(username=user.username, email=user.email)
            if user_ban:
                return error_banned(request, user, user_ban)
            if user.activation == User.ACTIVATION_NONE:
                return error403(request, Message(request, 'users/activation/not_required', extra={'user': user}))
            if user.activation == User.ACTIVATION_ADMIN:
                return error403(request, Message(request, 'users/activation/only_by_admin', extra={'user': user}))
            request.messages.set_flash(Message(request, 'users/activation/resent', extra={'user':user}), 'success')
            user.email_user(
                            request,
                            'users/activation/resend',
                            _("Account Activation"),
                            )
            return redirect(reverse('index'))
        else:
            message = Message(request, form.non_field_errors()[0], 'error')
    else:
        form = UserSendSpecialMailForm(request=request)
    return request.theme.render_to_response('users/resend_activation.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                            },
                                            context_instance=RequestContext(request));