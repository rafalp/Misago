from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from misago.admin.views import render as mi_render

from . import db_settings
from .forms import ChangeSettingsForm
from .models import SettingsGroup


def render(request, template, context=None):
    context = context or {}

    context['settings_groups'] = SettingsGroup.objects.ordered_alphabetically()

    if not 'active_group' in context:
        context['active_group'] = {'key': None}

    return mi_render(request, template, context)


def index(request):
    return render(request, 'misago/admin/conf/index.html')


def group(request, key):
    try:
        active_group = SettingsGroup.objects.get(key=key)
    except SettingsGroup.DoesNotExist:
        messages.error(request, _("Settings group could not be found."))
        return redirect('misago:admin:system:settings:index')

    fieldsets = ChangeSettingsForm(group=active_group)
    if request.method == 'POST':
        fieldsets = ChangeSettingsForm(request.POST, group=active_group)
        valid_fieldsets = len([True for fieldset in fieldsets if fieldset['form'].is_valid()])
        if len(fieldsets) == valid_fieldsets:
            new_values = {}
            for fieldset in fieldsets:
                new_values.update(fieldset['form'].cleaned_data)

            for setting in active_group.setting_set.all():
                setting.value = new_values[setting.setting]
                setting.save(update_fields=['dry_value'])

            db_settings.flush_cache()

            messages.success(request, _("Changes in settings have been saved!"))
            return redirect('misago:admin:system:settings:group', key=key)

    use_single_form_template = (len(fieldsets) == 1 and not fieldsets[0]['legend'])

    return render(
        request, 'misago/admin/conf/group.html', {
            'active_group': active_group,
            'fieldsets': fieldsets,
            'use_single_form_template': use_single_form_template,
        }
    )
