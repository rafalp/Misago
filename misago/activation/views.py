from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.banning.models import check_ban
from misago.banning.decorators import block_banned
from misago.banning.views import error_banned
from misago.forms.layouts import FormLayout
from misago.authn.methods import sign_user_in
from misago.authn.decorators import block_authenticated
from misago.activation.forms import UserSendActivationMailForm
from misago.bruteforce.decorators import block_jammed
from misago.messages import Message
from misago.users.models import User
from misago.views import redirect_message, error404


@block_banned
@block_authenticated
@block_jammed
def form(request):
    message = None
    if request.method == 'POST':
        form = UserSendActivationMailForm(request.POST, request=request)
        if form.is_valid():
            user = form.found_user
            user_ban = check_ban(username=user.username, email=user.email)
            
            if user_ban:
                return error_banned(request, user, user_ban)
            
            if user.activation == User.ACTIVATION_NONE:
                return redirect_message(request, Message(_("%(username)s, your account is already active.") % {'username': user.username}), 'info')
            
            if user.activation == User.ACTIVATION_ADMIN:
                return redirect_message(request, Message(_("%(username)s, only board administrator can activate your account.") % {'username': user.username}), 'info')
        
            user.email_user(
                            request,
                            'users/activation/resend',
                            _("Account Activation"),
                            )
            return redirect_message(request, Message(_("%(username)s, e-mail containing new activation link has been sent to %(email)s.") % {'username': user.username, 'email': user.email}), 'success')
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = UserSendActivationMailForm(request=request)
    return request.theme.render_to_response('resend_activation.html',
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
            return redirect_message(request, Message(_("%(username)s, your account is already active.") % {'username': user.username}), 'info')
            
        if user.activation == User.ACTIVATION_ADMIN:
            return redirect_message(request, Message(_("%(username)s, only board administrator can activate your account.") % {'username': user.username}), 'info')
        
        if not token or not user.token or user.token != token:
            return redirect_message(request, Message(_("%(username)s, your activation link is invalid. Try again or request new activation e-mail.") % {'username': user.username}), 'error')
        
        # Activate and sign in our member
        user.activation = User.ACTIVATION_NONE
        sign_user_in(request, user)
        
        # Update monitor
        request.monitor['users_inactive'] = int(request.monitor['users_inactive']) - 1
        
        if current_activation == User.ACTIVATION_CREDENTIALS:
            return redirect_message(request, Message(_("%(username)s, your account has been successfully reactivated after change of sign-in credentials.") % {'username': user.username}), 'success')
        else:
            return redirect_message(request, Message(_("%(username)s, your account has been successfully activated. Welcome aboard!") % {'username': user.username}), 'success')
    except User.DoesNotExist:
        return error404(request)