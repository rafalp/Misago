from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.banning.models import check_ban
from misago.banning.decorators import block_banned
from misago.banning.views import error_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security import get_random_string
from misago.security.decorators import *
from misago.resetpswd.forms import UserResetPasswordForm
from misago.users.models import User
from misago.views import redirect_message, error404


@block_banned
@block_authenticated
@block_jammed   
def form(request):
    message = None
    
    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST, request=request)
        
        if form.is_valid():
            user = form.found_user
            user_ban = check_ban(username=user.username, email=user.email)
            
            if user_ban:
                return error_banned(request, user, user_ban)
            elif user.activation != User.ACTIVATION_NONE:
                return redirect_message(request, Message(_("%(username)s, your account has to be activated in order for you to be able to request new password.") % {'username': user.username}), 'info')
            
            user.token = get_random_string(12)
            user.save(force_update=True)
            user.email_user(
                            request,
                            'users/password/confirm',
                            _("Confirm New Password Request")
                            )
            
            return redirect_message(request, Message(_("%(username)s, new password request confirmation has been sent to %{email}s.") % {'username': user.username, 'email': user.email}), 'info')
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = UserSendSpecialMailForm(request=request)
    return request.theme.render_to_response('reset_password.html',
                                            {
                                             'message': message,
                                             'form': FormLayout(form),
                                            },
                                            context_instance=RequestContext(request));


@block_banned
@block_authenticated
@block_jammed
def reset(request, username="", user="0", token=""):
    user = int(user)
    try:
        user = User.objects.get(pk=user)
        user_ban = check_ban(username=user.username, email=user.email)
        
        if user_ban:
            return error_banned(request, user, user_ban)
        
        if user.activation != User.ACTIVATION_NONE:
            return redirect_message(request, Message(_("%(username)s, your account has to be activated in order for you to be able to request new password.") % {'username': user.username}), 'info')
        
        if not token or not user.token or user.token != token:
            return redirect_message(request, Message(_("%(username)s, request confirmation link is invalid. Please request new confirmation link.") % {'username': user.username}), 'error')
        
        new_password = get_random_string(6)
        user.token = None
        user.set_password(new_password)
        user.save(force_update=True)
        
        # Logout signed in and kill remember me tokens
        Session.objects.filter(user=user).update(user=None)
        Token.objects.filter(user=user).delete()
        
        # Set flash and mail new password
        user.email_user(
                        request,
                        'users/password/new',
                        _("Your New Password"),
                        {'password': new_password}
                        )
        
        return redirect_message(request, Message(_("%(username)s, your password has been changed with new one that was sent to %{email}s.") % {'username': user.username, 'email': user.email}), 'success')
    except User.DoesNotExist:
        return error404(request)