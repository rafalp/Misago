from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from misago.banning.models import check_ban
from misago.security.models import SignInAttempt
from misago.sessions.models import Token
from misago.users.models import User
    
"""
Exception constants
"""
CREDENTIALS = 'security/bad_credentials'
ACTIVATION_USER = 'users/activation_user'
ACTIVATION_ADMIN = 'users/activation_admin'
BANNED = 'banned'
NOT_ADMIN = 'security/not_admin'


class AuthException(Exception):
    """
    Auth Exception is thrown when auth_* method finds problem with allowing user to sign-in
    """
    def __init__(self, type=None, user=None, ban=None):
        self.type = type
        self.user = user
        self.ban = ban
        
    def __str__(self):
        return self.error
      
    
def get_user(email, password, admin=False):
    """
    Fetch user from DB using email/pass pair, scream if either of data is incorrect
    """
    try:
        user = User.objects.get_by_email(email)
        if not user.check_password(password):
            raise AuthException(CREDENTIALS, user)
        if not admin:
            if user.activation == User.ACTIVATION_ADMIN:
                # Only admin can activate your account.
                raise AuthException(ACTIVATION_ADMIN, user)
            if user.activation != User.ACTIVATION_NONE:
                # Only admin can activate your account.
                raise AuthException(ACTIVATION_USER, user)
        
    except User.DoesNotExist:
        raise AuthException(CREDENTIALS)
    return user;


def auth_forum(request, email, password):
    """
    Forum auth - check bans and if we are in maintenance - maintenance access
    """
    user = get_user(email, password)
    user_ban = check_ban(username=user.username, email=user.email)
    if user_ban:
        raise AuthException(BANNED, user, user_ban)
    return user;


def auth_remember(request, ip):
    """
    Remember-me auth - check if token is valid
    Dont worry about AuthException being empty, it doesnt have to have anything
    """
    if request.firewall.admin:
        raise AuthException()
    if SignInAttempt.objects.is_jammed(request.settings, ip):
        raise AuthException()
    cookie_token = settings.COOKIES_PREFIX + 'TOKEN'
    try:
        cookie_token = request.COOKIES[cookie_token]
        if len(cookie_token) != 42:
            raise AuthException()
        try:
            token_rk = Token.objects.select_related().get(pk=cookie_token)
        except Token.DoesNotExist:
            request.cookie_jar.delete('TOKEN')
            raise AuthException()
        # See if token is not expired
        token_expires = timezone.now() - timedelta(days=request.settings['remember_me_lifetime'])
        if request.settings['remember_me_extensible'] and token_rk.accessed < token_expires:
            # Token expired because it's last use is smaller than expiration date
            raise AuthException()
        if not request.settings['remember_me_extensible'] and token_rk.created < token_expires:
            # Token expired because it was created before expiration date
            raise AuthException()
        # Update token date
        token_rk.accessed = timezone.now()
        token_rk.save(force_update=True)
        request.cookie_jar.set('TOKEN', token_rk.id, True)
    except (AttributeError, KeyError):
        raise AuthException()
    return token_rk


def auth_admin(request, email, password):
    """
    Admin auth - check ACP permissions
    """
    user = get_user(email, password, True)
    if not user.is_admin():
        raise AuthException(NOT_ADMIN)
    return user;


def sign_user_in(request, user):
    user.set_last_visit(
                        request.session.get_ip(request),
                        request.META.get('HTTP_USER_AGENT', ''),
                        )
    user.save(force_update=True)
    request.session.set_user(user)
    if request.settings['sessions_hidden']:
        request.session.set_hidden(user.hide_activity > 0)