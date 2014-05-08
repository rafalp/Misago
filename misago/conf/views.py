from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.admin.views import render as mi_render
from misago.conf.models import SettingsGroup, Setting


def render(request, template, context=None):
    context = context or {}

    context['settings_groups'] = SettingsGroup.objects.ordered_alphabetically()

    if not 'active_group' in context:
        context['active_group'] = {'key': None}

    return mi_render(request, template, context)


def index(request):
    return render(request, 'misago/admin/conf/index.html')


def group(request, group_key):
    try:
        active_group = SettingsGroup.objects.get(key=group_key)
    except SettingsGroup.DoesNotExist:
        messages.error(request, _("Settings group could not be found."))
        return redirect('misago:admin:settings:index')

    return render(request, 'misago/admin/conf/group.html',
                  {'active_group': active_group})
