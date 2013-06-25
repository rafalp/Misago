from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.apps.errors import error404, error_banned
from misago.auth import sign_user_in
from misago.decorators import block_authenticated, block_banned, block_crawlers, block_jammed
from misago.forms import FormLayout
from misago.messages import Message
from misago.models import Ban, User
from misago.shortcuts import redirect_message, render_to_response
from misago.apps.activation.forms import UserSendActivationMailForm

@block_crawlers
@block_banned
@block_authenticated
@block_jammed
def form(request):
    message = None
    if request.method == 'POST':
        form = UserSendActivationMailForm(request.POST, request=request)
        if form.is_valid():
            user = form.found_user
            user_ban = Ban.objects.check_ban(username=user.username, email=user.email)

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
    return render_to_response('resend_activation.html',
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
        user_ban = Ban.objects.check_ban(username=user.username, email=user.email)
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
        User.objects.resync_monitor(request.monitor)

        if current_activation == User.ACTIVATION_CREDENTIALS:
            return redirect_message(request, Message(_("%(username)s, your account has been successfully reactivated after change of sign-in credentials.") % {'username': user.username}), 'success')
        else:
            return redirect_message(request, Message(_("%(username)s, your account has been successfully activated. Welcome aboard!") % {'username': user.username}), 'success')
    except User.DoesNotExist:
        return error404(request)
