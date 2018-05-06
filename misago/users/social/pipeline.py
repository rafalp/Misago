from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from misago.conf import settings
from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned

from misago.users.models import Ban
from misago.users.bans import get_request_ip_ban, get_user_ban
from misago.users.validators import ValidationError, validate_username, validate_email

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
    
    email = details.get('email')
    username = kwargs.get('clean_username')
    
    if not email or not username:
        return None

    try:
        validate_email(email)
    except ValidationError:
        return None

    user = UserModel.objects.create_user(username, email, set_default_avatar=True)
    return {'user': user, 'is_new': True}


def create_user_with_form(strategy, details, backend, user=None, *args, **kwargs):
    """Alternatively to create_user lets user confirm account creation before authenticating"""
    if user:
        return None
