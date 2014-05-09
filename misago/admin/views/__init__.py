from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.shortcuts import render as dj_render
from misago.admin import site
from misago.admin.auth import is_admin_session, update_admin_session
from misago.admin.views.auth import login


__ALL__ = ['get_protected_namespace', 'render', 'protected_admin_view']


def get_protected_namespace(request):
    for namespace in settings.MISAGO_ADMIN_NAMESPACES:
        try:
            admin_path = reverse('%s:index' % namespace)
            if request.path.startswith(admin_path):
                return namespace
        except NoReverseMatch:
            pass
    else:
        return None


def render(request, template, context=None):
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
