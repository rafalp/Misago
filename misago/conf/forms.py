from django import forms
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext

from misago.core.forms import YesNoSwitch


__ALL__ = ['ChangeSettingsForm']


class ValidateChoicesNum(object):
    def __init__(self, min_choices=0, max_choices=0):
        self.min_choices = min_choices
        self.max_choices = max_choices

    def __call__(self, data):
        data_len = len(data)

        if self.min_choices and self.min_choices > data_len:
            message = ungettext(
                'You have to select at least %(choices)d option.',
                'You have to select at least %(choices)d options.',
                self.min_choices,
            )
            raise forms.ValidationError(message % {'choices': self.min_choices})

        if self.max_choices and self.max_choices < data_len:
            message = ungettext(
                'You cannot select more than %(choices)d option.',
                'You cannot select more than %(choices)d options.',
                self.max_choices,
            )
            raise forms.ValidationError(message % {'choices': self.max_choices})

        return data


def basic_kwargs(setting, extra):
    kwargs = {
        'label': _(setting.name),
        'initial': setting.value,
        'required': extra.get('min_length') or extra.get('min'),
    }

    if setting.description:
        kwargs['help_text'] = _(setting.description)

    if setting.form_field == 'yesno':
        # YesNoSwitch is int-base and setting is bool based
        # this means we need to do quick conversion
        kwargs['initial'] = 1 if kwargs['initial'] else 0

    if kwargs['required']:
        if kwargs.get('help_text'):
            format = {'help_text': kwargs['help_text']}
            kwargs['help_text'] = _('Required. %(help_text)s') % format
        else:
            kwargs['help_text'] = _('This field is required.')

    return kwargs


def localise_choices(extra):
    return [(v, _(l)) for v, l in extra.get('choices', [])]


def create_checkbox(setting, kwargs, extra):
    kwargs['widget'] = forms.CheckboxSelectMultiple()
    kwargs['choices'] = localise_choices(extra)

    if extra.get('min') or extra.get('max'):
        kwargs['validators'] = [ValidateChoicesNum(extra.pop('min', 0), extra.pop('max', 0))]

    if setting.python_type == 'int':
        return forms.TypedMultipleChoiceField(coerce='int', **kwargs)
    else:
        return forms.MultipleChoiceField(**kwargs)


def create_choice(setting, kwargs, extra):
    if setting.form_field == 'choice':
        kwargs['widget'] = forms.RadioSelect()
    else:
        kwargs['widget'] = forms.Select()

    kwargs['choices'] = localise_choices(extra)

    if setting.python_type == 'int':
        return forms.TypedChoiceField(coerce='int', **kwargs)
    else:
        return forms.ChoiceField(**kwargs)


def create_text(setting, kwargs, extra):
    kwargs.update(extra)
    if setting.python_type == 'int':
        return forms.IntegerField(**kwargs)
    else:
        return forms.CharField(**kwargs)


def create_textarea(setting, kwargs, extra):
    widget_kwargs = {}
    if extra.get('min_length', 0) == 0:
        kwargs['required'] = False
    if extra.get('rows', 0):
        widget_kwargs['attrs'] = {'rows': extra.pop('rows')}

    kwargs['widget'] = forms.Textarea(**widget_kwargs)
    return forms.CharField(**kwargs)


def create_yesno(setting, kwargs, extra):
    return YesNoSwitch(**kwargs)


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
    field_extra = setting.field_extra

    form_field = field_factory(setting, basic_kwargs(setting, field_extra), field_extra)

    FormType = type('FormType%s' % setting.pk, (FormType, ), {setting.setting: form_field})

    return FormType


def ChangeSettingsForm(data=None, group=None):
    """factory method that builds valid form for settings group"""

    class FormType(forms.Form):
        pass

    fieldsets = []

    fieldset_legend = None
    fieldset_form = FormType
    fieldset_fields = False
    for setting in group.setting_set.order_by('order'):
        if setting.legend and setting.legend != fieldset_legend:
            if fieldset_fields:
                fieldsets.append({
                    'legend': fieldset_legend,
                    'form': fieldset_form(data),
                })
            fieldset_legend = setting.legend
            fieldset_form = FormType
            fieldset_fields = False
        fieldset_fields = True
        fieldset_form = setting_field(fieldset_form, setting)

    if fieldset_fields:
        fieldsets.append({
            'legend': fieldset_legend,
            'form': fieldset_form(data),
        })

    return fieldsets
