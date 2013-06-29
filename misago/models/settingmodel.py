import base64
from django import forms
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from misago.utils.timezones import tzlist
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Setting(models.Model):
    setting = models.CharField(max_length=255, primary_key=True)
    group = models.ForeignKey('SettingsGroup', to_field='key')
    _value = models.TextField(db_column='value', null=True, blank=True)
    value_default = models.TextField(null=True, blank=True)
    normalize_to = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    extra = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    separator = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        app_label = 'misago'

    def get_extra(self):
        return pickle.loads(base64.decodestring(self.extra))

    @property
    def value(self):
        if self.normalize_to == 'array':
            return self._value.split(',')
        if self.normalize_to == 'integer':
            return int(self._value)
        if self.normalize_to == 'float':
            return float(self._value)
        if self.normalize_to == 'boolean':
            return self._value == "1"
        return self._value

    @value.setter
    def value(self, value):
        if self.normalize_to == 'array':
            self._value = ','.join(value)
        elif self.normalize_to == 'integer':
            self._value = int(value)
        elif self.normalize_to == 'float':
            self._value = float(value)
        elif self.normalize_to == 'boolean':
            self._value = 1 if value else 0
        else:
            self._value = value
        if not self._value and self.value_default:
            self._value = self.value_default
        return self._value

    def get_field(self):
        from misago.forms import YesNoSwitch
        
        extra = self.get_extra()

        # Set validators
        field_validators = []
        if 'min' in extra:
            if self.normalize_to == 'string' or self.normalize_to == 'array':
                field_validators.append(validators.MinLengthValidator(extra['min']))
            if self.normalize_to == 'integer' or self.normalize_to == 'float':
                field_validators.append(validators.MinValueValidator(extra['min']))
        if 'max' in extra:
            if self.normalize_to == 'string' or self.normalize_to == 'array':
                field_validators.append(validators.MaxLengthValidator(extra['max']))
            if self.normalize_to == 'integer' or self.normalize_to == 'float':
                field_validators.append(validators.MaxValueValidator(extra['max']))

        # Yes-no
        if self.field == 'yesno':
            return forms.BooleanField(
                                   initial=self.get_value(),
                                   label=_(self.name),
                                   help_text=_(self.description) if self.description else None,
                                   required=False,
                                   widget=YesNoSwitch,
                                   )

        # Multi-list
        if self.field == 'mlist':
            return forms.MultipleChoiceField(
                                     initial=self.get_value(),
                                     label=_(self.name),
                                     help_text=_(self.description) if self.description else None,
                                     widget=forms.CheckboxSelectMultiple,
                                     validators=field_validators,
                                     required=False,
                                     choices=extra['choices']
                                     )

        # Select or choice
        if self.field == 'select' or self.field == 'choice':
            # Timezone list?
            if extra['choices'] == '#TZ#':
                extra['choices'] = tzlist()
            return forms.ChoiceField(
                                     initial=self.get_value(),
                                     label=_(self.name),
                                     help_text=_(self.description) if self.description else None,
                                     widget=forms.RadioSelect if self.field == 'choice' else forms.Select,
                                     validators=field_validators,
                                     required=False,
                                     choices=extra['choices']
                                     )

        # Textarea
        if self.field == 'textarea':
            return forms.CharField(
                                   initial=self.get_value(),
                                   label=_(self.name),
                                   help_text=_(self.description) if self.description else None,
                                   validators=field_validators,
                                   required=False,
                                   widget=forms.Textarea
                                   )

        # Default input
        default_input = forms.CharField
        if self.normalize_to == 'integer':
            default_input = forms.IntegerField
        if self.normalize_to == 'float':
            default_input = forms.FloatField

        # Make text-input
        return default_input(
                             initial=self.get_value(),
                             label=_(self.name),
                             help_text=_(self.description) if self.description else None,
                             validators=field_validators,
                             required=False,
                             )
