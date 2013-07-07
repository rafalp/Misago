from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ungettext, ugettext as _
from misago.conf import settings as misago_settings
from misago.forms import Form, FormLayout, FormFields
from misago.messages import Message
from misago.search import SearchQuery, SearchException
from misago.models import SettingsGroup, Setting
from misago.shortcuts import render_to_response
from misago.apps.errors import error404
from misago.apps.admin.settings.forms import SearchForm

def settings(request, group_id=None, group_slug=None):
    # Load groups and find selected group
    settings_groups = SettingsGroup.objects.all().order_by('key')
    if not group_id:
        active_group = settings_groups[0]
        group_id = active_group.pk
    else:
        group_id = int(group_id)
        for group in settings_groups:
            if group.pk == group_id:
                active_group = group
                break
        else:
            return error404(request, _('Requested settings group could not be found.'))

    # Load selected group settings and turn them into form
    group_settings = Setting.objects.filter(group=active_group).order_by('position')
    last_fieldset = (None, [])
    group_form = {'layout': []}
    for setting in group_settings:
        # New field subgroup?
        if setting.separator and last_fieldset[0] != setting.separator:
            if last_fieldset[0]:
                group_form['layout'].append(last_fieldset)
            last_fieldset = (_(setting.separator), [])
        last_fieldset[1].append(setting.pk)
        group_form[setting.pk] = setting.get_field()
    group_form['layout'].append(last_fieldset)
    SettingsGroupForm = type('SettingsGroupForm', (Form,), group_form)

    #Submit form
    message = request.messages.get_message('admin_settings')
    if request.method == 'POST':
        form = SettingsGroupForm(request.POST, request=request)
        if form.is_valid():
            for setting in form.cleaned_data.keys():
                misago_settings[setting] = form.cleaned_data[setting]
            cache.delete('settings')
            request.messages.set_flash(Message(_('Configuration has been changed.')), 'success', 'admin_settings')
            return redirect(reverse('admin_settings', kwargs={
                                                       'group_id': active_group.pk,
                                                       'group_slug': active_group.key,
                                                       }))
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = SettingsGroupForm(request=request)

    # Display settings group form      
    return render_to_response('settings/settings.html',
                              {
                              'message': message,
                              'groups': settings_groups,
                              'active_group': active_group,
                              'search_form': FormFields(SearchForm(request=request)),
                              'form': FormLayout(form),
                              'raw_form': form,
                              },
                              context_instance=RequestContext(request));


def settings_search(request):
    settings_groups = SettingsGroup.objects.all().order_by('key')
    message = None
    found_settings = []
    try:
        if request.method == 'POST' and request.csrf.request_secure(request):
            form = SearchForm(request.POST, request=request)
            if form.is_valid():
                # Start search
                search_strings = SearchQuery(form.cleaned_data['search_text'])

                # Loop over groups using our search query
                for setting in Setting.objects.all().order_by('setting'):
                    if (search_strings.search(_(setting.name))
                        or (setting.description and search_strings.search(_(setting.description)))
                        or (setting.value and search_strings.search(setting.value))):
                        found_settings.append(setting)

                # Scream if nothing could be found
                if found_settings:
                    message = Message(ungettext(
                                                'One setting that matches search criteria has been found.',
                                                '%(count)d settings that match search criteria have been found.',
                                                len(found_settings)) % {
                                                    'count': len(found_settings),
                                                }, 'success')
                else:
                    raise SearchException(_('No settings that match search criteria have been found.'))
            else:
                raise SearchException(_('Search query is empty.'))
        else:
            raise SearchException(_('Search query is invalid.'))
    except SearchException as e:
        message = Message(unicode(e), 'error')
    return render_to_response('settings/search_results.html',
                              {
                              'message': message,
                              'groups': settings_groups,
                              'active_group': None,
                              'found_settings': found_settings,
                              'search_form': FormFields(form),
                              },
                              context_instance=RequestContext(request));
