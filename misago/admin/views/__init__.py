from django.urls import reverse, NoReverseMatch
from django.utils.translation import get_language
from django.shortcuts import render as dj_render

from ...conf import settings
from ...core.momentjs import get_locale_url
from .. import site
from ..auth import is_admin_authorized, update_admin_authorization
from ..momentjs import MISAGO_ADMIN_MOMENT_LOCALES
from .auth import login


def get_protected_namespace(request):
    for namespace in settings.MISAGO_ADMIN_NAMESPACES:
        try:
            admin_path = reverse("%s:index" % namespace)
            if request.path.startswith(admin_path):
                return namespace
        except NoReverseMatch:
            pass


def render(request, template, context=None, error_page=False):
    context = context or {}

    navigation = site.visible_branches(request)
    sections = navigation[0]

    try:
        actions = navigation[1]
    except IndexError:
        actions = []

    context.update({"sections": sections, "actions": actions})

    if error_page:
        # admittedly haxy solution for displaying navs on error pages
        context["actions"] = []
        context["pages"] = []
        for item in sections:
            item["is_active"] = False
    else:
        context["active_section"] = None
        for item in sections:
            if item["is_active"]:
                context["active_section"] = item
                break

        context["active_link"] = None
        for nav in navigation:
            for item in nav:
                if item["is_active"]:
                    context["active_link"] = item
                    break

    context["ADMIN_MOMENTJS_LOCALE_URL"] = get_admin_moment_locale_url()

    return dj_render(request, template, context)


def get_admin_moment_locale_url():
    return get_locale_url(
        get_language(),
        static_path_template="misago/admin/momentjs/%s.js",
        locales=MISAGO_ADMIN_MOMENT_LOCALES,
    )


# Decorator for views
def protected_admin_view(f):
    def decorator(request, *args, **kwargs):
        protected_view = get_protected_namespace(request)
        if protected_view:
            if is_admin_authorized(request):
                update_admin_authorization(request)
                return f(request, *args, **kwargs)
            request.admin_namespace = protected_view
            return login(request)
        return f(request, *args, **kwargs)

    return decorator
