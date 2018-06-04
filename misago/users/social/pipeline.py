import json

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext as _
from social_core.pipeline.partial import partial

from misago.conf import settings
from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned

from misago.users.bans import get_request_ip_ban, get_user_ban
from misago.users.forms.register import SocialAuthRegisterForm
from misago.users.models import Ban
from misago.users.registration import get_registration_result_json, send_welcome_email
from misago.users.validators import (
    ValidationError, validate_new_registration, validate_email, validate_username)

from .utils import get_social_auth_backend_name, perpare_username


UserModel = get_user_model()


def validate_ip_not_banned(strategy, details, backend, user=None, *args, **kwargs):
    """Pipeline step that interrupts pipeline if found user is non-staff and IP banned"""
    if not user or user.is_staff:
        return None
    
    ban = get_request_ip_ban(strategy.request)
    if ban:
        hydrated_ban = Ban(
            check_type=Ban.IP,
            user_message=ban['message'],
            expires_on=ban['expires_on'],
        )
        raise SocialAuthBanned(backend, hydrated_ban)


def validate_user_not_banned(strategy, details, backend, user=None, *args, **kwargs):
    """Pipeline step that interrupts pipeline if found user is non-staff and banned"""
    if not user or user.is_staff:
        return None

    user_ban = get_user_ban(user)
    if user_ban:
        raise SocialAuthBanned(backend, user_ban)


def associate_by_email(strategy, details, backend, user=None, *args, **kwargs):
    """If user with e-mail from provider exists in database and is active,
    this step authenticates them.
    """
    if user:
        return None

    email = details.get('email')
    if not email:
        return None

    try:
        user = UserModel.objects.get_by_email(email)
    except UserModel.DoesNotExist:
        return None

    backend_name = get_social_auth_backend_name(backend.name)

    if not user.is_active:
        raise SocialAuthFailed(
            backend,
            _(
                "The e-mail address associated with your %(backend)s account is "
                "not available for use on this site."
            ) % {'backend': backend_name}
        )

    if user.requires_activation_by_admin:
        raise SocialAuthFailed(
            backend,
            _(
                "Your account has to be activated by site administrator before you will be able to "
                "sign in with %(backend)s."
            ) % {'backend': backend_name}
        )

    return {'user': user, 'is_new': False}


def get_username(strategy, details, backend, user=None, *args, **kwargs):
    """Resolve valid username for use in new account"""
    if user:
        return None

    username = perpare_username(details.get('username', ''))
    full_name = perpare_username(details.get('full_name', ''))
    first_name = perpare_username(details.get('first_name', ''))
    last_name = perpare_username(details.get('last_name', ''))

    names_to_try = [
        username,
        first_name,
    ]

    if username:
        names_to_try.append(username)

    if first_name:
        names_to_try.append(first_name)
        if last_name:
            # if first name is taken, try first name + first char of last name
            names_to_try.append(first_name + last_name[0])

    if full_name:
        names_to_try.append(full_name)

    username_length_max = settings.username_length_max
    for name in names_to_try:
        if len(name) > username_length_max:
            names_to_try.append(name[:username_length_max])

    for name in filter(bool, names_to_try):
        try:
            validate_username(name)
            return {'clean_username': name}
        except ValidationError:
            pass


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """Aggressively attempt to register and sign in new user"""
    if user:
        return None
    
    request = strategy.request
    email = details.get('email')
    username = kwargs.get('clean_username')
    
    if not email or not username:
        return None

    try:
        validate_email(email)
        validate_new_registration(request, {
            'email': email,
            'username': username,
        })
    except ValidationError:
        return None

    activation_kwargs = {}
    if settings.account_activation == 'admin':
        activation_kwargs = {'requires_activation': UserModel.ACTIVATION_ADMIN}

    new_user = UserModel.objects.create_user(
        username, 
        email, 
        create_audit_trail=True,
        joined_from_ip=request.user_ip, 
        set_default_avatar=True,
        **activation_kwargs
    )

    send_welcome_email(request, new_user)

    return {'user': new_user, 'is_new': True}


@partial
def create_user_with_form(strategy, details, backend, user=None, *args, **kwargs):
    """Alternatively to create_user lets user confirm account creation before authenticating"""
    if user:
        return None

    request = strategy.request
    backend_name = get_social_auth_backend_name(backend.name)

    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
        except (TypeError, ValueError):
            request_data = request.POST.copy()
            
        form = SocialAuthRegisterForm(request_data, request=request)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)

        email_verified = form.cleaned_data['email'] == details.get('email')

        activation_kwargs = {}
        if settings.account_activation == 'admin':
            activation_kwargs = {'requires_activation': UserModel.ACTIVATION_ADMIN}
        elif settings.account_activation == 'user' and not email_verified:
            activation_kwargs = {'requires_activation': UserModel.ACTIVATION_USER}

        try:
            new_user = UserModel.objects.create_user(
                form.cleaned_data['username'],
                form.cleaned_data['email'],
                create_audit_trail=True,
                joined_from_ip=request.user_ip,
                set_default_avatar=True,
                **activation_kwargs
            )
        except IntegrityError:
            return JsonResponse({'__all__': _("Please try resubmitting the form.")}, status=400)

        send_welcome_email(request, new_user)

        return {'user': new_user, 'is_new': True}

    request.frontend_context['SOCIAL_AUTH'] = {
        'backend_name': backend_name,
        'step': 'register',
        'email': details.get('email'),
        'username': kwargs.get('clean_username'),
        'url': reverse('social:complete', kwargs={'backend': backend.name}),
    }

    return render(request, 'misago/socialauth.html', {
        'backend_name': backend_name,
    })


@partial
def require_activation(strategy, details, backend, user=None, is_new=False, *args, **kwargs):
    if not user:
        # Social auth pipeline has entered corrupted state
        # Remove partial auth state and redirect user to beginning
        partial_token = strategy.session.get('partial_pipeline_token')
        if partial_token:
            strategy.clean_partial_pipeline(partial_token)
        return None
        
    if not user.requires_activation:
        return None

    request = strategy.request
    backend_name = get_social_auth_backend_name(backend.name)

    response_data = get_registration_result_json(user)
    response_data.update({'step': 'done',  'backend_name': backend_name})

    if request.method == 'POST':
        # we are carrying on from requestration request
        return JsonResponse(response_data)

    request.frontend_context['SOCIAL_AUTH'] = response_data
    request.frontend_context['SOCIAL_AUTH'].update({
        'url': reverse('social:complete', kwargs={'backend': backend.name}),
    })

    return render(request, 'misago/socialauth.html', {
        'backend_name': backend_name,
    })
