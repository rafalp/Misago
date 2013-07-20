from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.auth import sign_user_in
from misago.conf import settings
from misago.decorators import block_authenticated, block_banned, block_crawlers, block_jammed
from misago import messages
from misago.messages import Message
from misago.models import SignInAttempt, User
from misago.shortcuts import redirect_message, render_to_response
from misago.apps.register.forms import UserRegisterForm

@block_crawlers
@block_banned
@block_authenticated
@block_jammed
def form(request):
    if settings.account_activation == 'block':
       return redirect_message(request, messages.INFO, _("We are sorry but we don't allow new members registrations at this time."))

    message = None
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request=request)
        if form.is_valid():
            need_activation = 0
            if settings.account_activation == 'user':
                need_activation = User.ACTIVATION_USER
            if settings.account_activation == 'admin':
                need_activation = User.ACTIVATION_ADMIN

            new_user = User.objects.create_user(
                                                form.cleaned_data['username'],
                                                form.cleaned_data['email'],
                                                form.cleaned_data['password'],
                                                ip=request.session.get_ip(request),
                                                agent=request.META.get('HTTP_USER_AGENT'),
                                                activation=need_activation,
                                                request=request
                                                )

            if need_activation == User.ACTIVATION_NONE:
                # Sign in user
                sign_user_in(request, new_user)
                messages.success(request, _("Welcome aboard, %(username)s! Your account has been registered successfully.") % {'username': new_user.username})

            if need_activation == User.ACTIVATION_USER:
                # Mail user activation e-mail
                messages.info(request, _("%(username)s, your account has been registered, but you will have to activate it before you will be able to sign-in. We have sent you an e-mail with activation link.") % {'username': new_user.username})
                new_user.email_user(
                                    request,
                                    'users/activation/user',
                                    _("Welcome aboard, %(username)s!") % {'username': new_user.username},
                                    )

            if need_activation == User.ACTIVATION_ADMIN:
                # Require admin activation
                messages.info(request, _("%(username)s, Your account has been registered, but you won't be able to sign in until board administrator accepts it. We'll notify when this happens. Thank you for your patience!") % {'username': new_user.username})
                new_user.email_user(
                                    request,
                                    'users/activation/admin',
                                    _("Welcome aboard, %(username)s!") % {'username': new_user.username},
                                    {'password': form.cleaned_data['password']}
                                    )

            User.objects.resync_monitor()
            return redirect(reverse('index'))
        else:
            message = Message(form.non_field_errors()[0], messages.ERROR)
            if settings.registrations_jams:
                SignInAttempt.objects.register_attempt(request.session.get_ip(request))
            # Have we jammed our account?
            if SignInAttempt.objects.is_jammed(request.session.get_ip(request)):
                request.jam.expires = timezone.now()
                return redirect(reverse('register'))
    else:
        form = UserRegisterForm(request=request)
    return render_to_response('register.html',
                              {
                              'message': message,
                              'form': form,
                              'hide_signin': True,
                              },
                              context_instance=RequestContext(request));