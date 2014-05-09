from django.utils.translation import ugettext_lazy as _
from misago.core import forms


__ALL__ = ['ChangeSettingsForm']


def basic_kwargs(setting):
    kwargs = {
        'label': _(setting.name),
        'initial': setting.value
    }
    if setting.description:
        kwargs['help_text'] = _(setting.description)

    return kwargs


def create_checkbox(setting, kwargs, extra):
    kwargs = basic_kwargs(setting)
    kwargs['widget'] = forms.CheckboxSelectMultiple()
    kwargs['choices'] = extra.get('choices', [])

    if setting.python_type == 'int':
        return forms.TypedMultipleChoiceField(coerce='int', **kwargs)
    else:
        return forms.MultipleChoiceField(**kwargs)


def create_choice(setting, kwargs, extra):
    kwargs = basic_kwargs(setting)
    if setting.form_field == 'choice':
        kwargs['widget'] = forms.RadioSelect()
    else:
        kwargs['widget'] = forms.Select()
    kwargs['choices'] = extra.get('choices', [])

    if kwargs['choices'] == '#tz#':
        pass

    if setting.python_type == 'int':
        return forms.TypedChoiceField(coerce='int', **kwargs)
    else:
        return forms.ChoiceField(**kwargs)


def create_text(setting, kwargs, extra):
    kwargs.update(extra)
    if setting.python_type == 'int':
        return forms.IntegerField(**kwargs)
    else:
        if extra.get('min_length', 0) == 0:
            kwargs['required'] = False
        return forms.CharField(**kwargs)


def create_textarea(setting, kwargs, extra):
    kwargs = basic_kwargs(setting)
    widget_kwargs = {}
    if extra.get('min_length', 0) == 0:
        kwargs['required'] = False
    if extra.get('rows', 0):
        widget_kwargs['attrs'] = {'rows': extra.pop('rows')}

    kwargs['widget'] = forms.Textarea(**widget_kwargs)
    return forms.CharField(**kwargs)


def create_yesno(setting, kwargs, extra):
    kwargs = basic_kwargs(setting)
    kwargs['widget'] = forms.RadioSelect()
    kwargs['choices'] = ((0, _('No')), (1, _('Yes')))
    return forms.TypedChoiceField(coerce='int', **kwargs)


FIELD_STYPES = {
    'checkbox': create_checkbox,
    'radio': create_choice,
    'select': create_choice,
    'text': create_text,
    'textarea': create_textarea,
    'yesno': create_yesno,
}


def setting_field(FormType, setting):
    field_factory = FIELD_STYPES[setting.form_field]
    form_field = field_factory(setting,
                               basic_kwargs(setting),
                               setting.field_extra)

    if setting.legend:
        form_field.legend = _(setting.legend)

    FormType = type('FormType%s' % setting.pk, (FormType,),
                    {setting.setting: form_field})

    return FormType


def ChangeSettingsForm(data=None, group=None):
    """
    Factory method that builds valid form for settings group
    """
    class FormType(forms.Form):
        pass

    fieldsets = []

    fieldset_legend = None
    fieldset_form = FormType
    fieldset_fields = False
    for setting in group.setting_set.order_by('order'):
        if setting.legend and setting.legend != fieldset_legend:
            if fieldset_fields != False:
                fieldsets.append(
                    {'legend': fieldset_legend, 'form': fieldset_form(data)})
            fieldset_legend = setting.legend
            fieldset_form = FormType
            fieldset_fields = False
        fieldset_fields = True
        fieldset_form = setting_field(fieldset_form, setting)

    if fieldset_fields:
        fieldsets.append(
            {'legend': fieldset_legend, 'form': fieldset_form(data)})

    return fieldsets
