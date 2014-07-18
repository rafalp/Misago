from django.shortcuts import redirect, render as django_render

from misago.users.sites import usercp


def render(request, template, context=None):
    context = context or {}
    context['pages'] = usercp.get_pages(request, context['profile'])
    return django_render(request, template, context)


def change_forum_options(request):
    pass


def change_sigin_credentials(request):
    pass


def change_username(request):
    pass
