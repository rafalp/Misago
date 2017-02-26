from django.urls import reverse, NoReverseMatch
from django.shortcuts import render as dj_render

from misago.conf import settings

from misago.admin import site
from misago.admin.auth import is_admin_session, update_admin_session
from .auth import login


def get_protected_namespace(request):
    for namespace in settings.MISAGO_ADMIN_NAMESPACES:
        try:
            admin_path = reverse('%s:index' % namespace)
            if request.path_info.startswith(admin_path):
                return namespace
        except NoReverseMatch:
            pass
    else:
        return None


def render(request, template, context=None, error_page=False):
    context = context or {}

    navigation = site.visible_branches(request)
    sections = navigation[0]

    try:
        actions = navigation[1]
    except IndexError:
        actions = []

    try:
        pages = navigation[2]
    except IndexError:
        pages = []

    context.update({'sections': sections, 'actions': actions, 'pages': pages})

    if error_page:
        # admittedly haxy solution for displaying navs on error pages
        context['actions'] = []
        context['pages'] = []
        for item in navigation[0]:
            item['is_active'] = False
    else:
        context['active_link'] = None
        for item in navigation[-1]:
            if item['is_active']:
                context['active_link'] = item
                break

    return dj_render(request, template, context)


# Decorator for views
def protected_admin_view(f):
    def decorator(request, *args, **kwargs):
        protected_view = get_protected_namespace(request)
        if protected_view:
            if is_admin_session(request):
                update_admin_session(request)
                return f(request, *args, **kwargs)
            else:
                request.admin_namespace = protected_view
                return login(request)
        else:
            return f(request, *args, **kwargs)

    return decorator
