from django.shortcuts import redirect, render as django_render


def render(request, template, context=None):
    context = context or {}

    if 'active_link' not in context:
        namespace = request.resolver_match.namespace
        url_name = request.resolver_match.url_name

        if namespace:
            active_link = '%s:%s' (namespace, url_name)
        else:
            active_link = url_name
        context['active_link'] = active_link

    return django_render(request, template, context)


def change_forum_options(request):
    pass


def change_sigin_credentials(request):
    pass


def change_username(request):
    pass
