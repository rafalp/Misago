from hashlib import md5
from time import time

from django.contrib import auth as dj_auth
from django.contrib import messages
from django.utils.translation import gettext as _

from ..conf import settings

TOKEN_KEY = "misago_admin_session_token"
UPDATED_KEY = "misago_admin_session_updated"

# Admin session state controls
def is_admin_authorized(request):
    if request.user.is_anonymous:
        return False

    if not request.user.is_staff:
        return False

    admin_token = request.session.get(TOKEN_KEY)
    if not admin_token == make_user_admin_token(request.user):
        return False

    updated = request.session.get(UPDATED_KEY, 0)
    if updated < time() - (settings.MISAGO_ADMIN_SESSION_EXPIRATION * 60):
        if updated:
            request.session.pop(UPDATED_KEY, None)
            messages.info(request, _("Your admin session has expired."))
        return False

    return True


def authorize_admin(request):
    request.session[TOKEN_KEY] = make_user_admin_token(request.user)
    request.session[UPDATED_KEY] = int(time())


def update_admin_authorization(request):
    request.session[UPDATED_KEY] = int(time())


def remove_admin_authorization(request):
    request.session.pop(TOKEN_KEY, None)
    request.session.pop(UPDATED_KEY, None)


def make_user_admin_token(user):
    formula = (str(user.pk), user.email, user.password, settings.SECRET_KEY)
    return md5(":".join(formula).encode()).hexdigest()


# Login/logout exposed
login = dj_auth.login
logout = dj_auth.logout


# Register signal for logout to make sure eventual admin session is closed
def django_login_handler(sender, **kwargs):
    request, user = kwargs["request"], kwargs["user"]
    try:
        admin_namespace = request.admin_namespace
    except AttributeError:
        admin_namespace = False
    if admin_namespace and user.is_staff:
        authorize_admin(request)


dj_auth.signals.user_logged_in.connect(django_login_handler)


def django_logout_handler(sender, **kwargs):
    remove_admin_authorization(kwargs["request"])


dj_auth.signals.user_logged_out.connect(django_logout_handler)
