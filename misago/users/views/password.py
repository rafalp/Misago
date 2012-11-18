from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.banning.models import check_ban
from misago.banning.decorators import block_banned
from misago.banning.views import error_banned
from misago.forms.layouts import FormLayout
from misago.messages import Message
from misago.security import get_random_string
from misago.security.decorators import *
from misago.users.forms import *
from misago.users.models import User
from misago.views import error403, error404


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
            elif user.activation != User.ACTIVATION_NONE:
                return error403(request, Message(request, 'users/activations/required', {'user': user}))
            user.token = get_random_string(12)
            user.save(force_update=True)
            request.messages.set_flash(Message(request, 'users/passwords/reset_confirm', extra={'user':user}), 'success')
            user.email_user(
                            request,
                            'users/reset_confirm',
                            _("Confirm New Password Request")
                            )
            return redirect(reverse('index'))
        else:
            message = Message(request, form.non_field_errors()[0])
    else:
        form = UserSendSpecialMailForm(request=request)
    return request.theme.render_to_response('users/forgot_password.html',
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
            return error403(request, Message(request, 'users/activations/required', {'user': user}))
        if not token or not user.token or user.token != token:
            return error403(request, Message(request, 'users/invalid_confirmation_link', {'user': user}))
        new_password = get_random_string(6)
        user.token = None
        user.set_password(new_password)
        user.save(force_update=True)
        # Logout signed in and kill remember me tokens
        Session.objects.filter(user=user).update(user=None)
        Token.objects.filter(user=user).delete()
        # Set flash and mail new password
        request.messages.set_flash(Message(request, 'users/passwords/reset_done', extra={'user':user}), 'success')
        user.email_user(
                        request,
                        'users/reset_new',
                        _("Your New Password"),
                        {'password': new_password}
                        )
        return redirect(reverse('sign_in'))
    except User.DoesNotExist:
        return error404(request)