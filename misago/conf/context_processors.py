from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils.translation import get_language

from .gateway import settings as misago_settings  # noqa
from .gateway import db_settings


LOGO_URL = static(misago_settings.MISAGO_LOGO)
BLANK_AVATAR_URL = static(misago_settings.MISAGO_BLANK_AVATAR)

STYLE = misago_settings._MISAGO_STYLE_DEFAULT.copy()

if misago_settings.MISAGO_STYLE:
    STYLE.update(MISAGO_STYLE)


def settings(request):
    return {
        'MISAGO_STYLE': STYLE,
        'DEBUG': misago_settings.DEBUG,
        'LANGUAGE_CODE_SHORT': get_language()[:2],
        'misago_settings': db_settings,
        'LOGO_URL': LOGO_URL,
        'BLANK_AVATAR_URL': BLANK_AVATAR_URL,
        'THREADS_ON_INDEX': misago_settings.MISAGO_THREADS_ON_INDEX,
        'LOGIN_REDIRECT_URL': misago_settings.LOGIN_REDIRECT_URL,
        'LOGIN_URL': misago_settings.LOGIN_URL,
        'LOGOUT_URL': misago_settings.LOGOUT_URL,
    }


def preload_settings_json(request):
    request.frontend_context['conf'].update(db_settings.get_public_settings())
    request.frontend_context['conf'].update({
        'csrf_cookie_name': misago_settings.CSRF_COOKIE_NAME,
        'threads_on_index': misago_settings.MISAGO_THREADS_ON_INDEX,
        'enable_delete_own_account': misago_settings.MISAGO_ENABLE_DELETE_OWN_ACCOUNT,
        'style': STYLE,
    })

    request.frontend_context['url'].update({
        'index': reverse('misago:index'),
        'blank_avatar': BLANK_AVATAR_URL,
        'logo': LOGO_URL,
        'login_redirect': reverse(misago_settings.LOGIN_REDIRECT_URL),
        'login': reverse(misago_settings.LOGIN_URL),
        'logout': reverse(misago_settings.LOGOUT_URL),
        'static': misago_settings.STATIC_URL,
    })

    return {}
