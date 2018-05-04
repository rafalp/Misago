from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from misago.core.exceptions import SocialAuthFailed, SocialAuthBanned

from misago.users.bans import get_request_ip_ban, get_user_ban

from .utils import get_social_auth_backend_name


UserModel = get_user_model()


def validate_ip_not_banned(strategy, details, backend, user=None, *args, **kwargs):
    """Pipeline step that interrupts pipeline if found user is non-staff and IP banned"""
    if user and user.acl.is_staff:
        return None
    
    ip_ban = get_request_ip_ban(strategy.request)
    if ip_ban:
        raise SocialAuthBanned(ip_ban)


def validate_user_not_banned(strategy, details, backend, user=None, *args, **kwargs):
    """Pipeline step that interrupts pipeline if found user is non-staff and banned"""
    if user and user.acl.is_staff:
        return None

    user_ban = get_user_ban(user)
    if user_ban:
        raise SocialAuthBanned(user_ban)


def associate_by_email(strategy, details, backend, user=None, *args, **kwargs):
    """If user with e-mail from provider exists in database and is active,
    this step authenticates them.
    """
    if user:
        return None

    email = details.get('email')
    if not email:
        return

    try:
        user = UserModel.objects.get_by_email(email)
    except UserModel.DoesNotExist:
        return None

    if not user.is_active:
        backend_name = get_social_auth_backend_name(backend.name)
        raise SocialAuthFailed(
            backend,
            _(
                "The e-mail address associated with your %(backend)s account is "
                "not available for use on this site."
            ) % {'backend': backend_name}
        )

    return {'user': user, 'is_new': False}


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """Aggressively attempt to register and sign in new user"""
    if user:
        return None


def create_user_with_form(strategy, details, backend, user=None, *args, **kwargs):
    """Alternatively to create_user lets user confirm account creation before authenticating"""
    if user:
        return None
