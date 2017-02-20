from hashlib import md5
from time import time

from django.contrib import auth as dj_auth
from django.contrib import messages
from django.utils.translation import ugettext as _

from misago.conf import settings


KEY_TOKEN = 'misago_admin_session_token'
KEY_UPDATED = 'misago_admin_session_updated'


def make_user_admin_token(user):
    formula = (str(user.pk), user.email, user.password, settings.SECRET_KEY)
    return md5(':'.join(formula).encode()).hexdigest()


# Admin session state controls
def is_admin_session(request):
    if request.user.is_anonymous:
        return False

    if not request.user.is_staff:
        return False

    admin_token = request.session.get(KEY_TOKEN)
    if not admin_token == make_user_admin_token(request.user):
        return False

    updated = request.session.get(KEY_UPDATED, 0)
    if updated < time() - (settings.MISAGO_ADMIN_SESSION_EXPIRATION * 60):
        if updated:
            request.session.pop(KEY_UPDATED, None)
            messages.info(request, _("Your admin session has expired."))
        return False

    return True


def start_admin_session(request, user):
    request.session[KEY_TOKEN] = make_user_admin_token(user)
    request.session[KEY_UPDATED] = int(time())


def update_admin_session(request):
    request.session[KEY_UPDATED] = int(time())


def close_admin_session(request):
    request.session.pop(KEY_TOKEN, None)
    request.session.pop(KEY_UPDATED, None)


# Login/logout exposed
login = dj_auth.login
logout = dj_auth.logout


# Register signal for logout to make sure eventual admin session is closed
def django_login_handler(sender, **kwargs):
    request, user = kwargs['request'], kwargs['user']
    try:
        admin_namespace = request.admin_namespace
    except AttributeError:
        admin_namespace = False
    if admin_namespace and user.is_staff:
        start_admin_session(request, user)


dj_auth.signals.user_logged_in.connect(django_login_handler)


def django_logout_handler(sender, **kwargs):
    close_admin_session(kwargs['request'])


dj_auth.signals.user_logged_out.connect(django_logout_handler)
