import base64
from django import forms
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from misago.forms import YesNoSwitch
from misago.timezones import tzlist
try:
    import cPickle as pickle
except ImportError:
    import pickle

class Group(models.Model):
    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def is_active(self, active_group):
        try:
            return self.pk == active_group.pk
        except AttributeError:
            return False

class Setting(models.Model):
    setting = models.CharField(max_length=255, primary_key=True)
    group = models.ForeignKey('Group', to_field='key')
    value = models.TextField(null=True, blank=True)
    value_default = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255)
    input = models.CharField(max_length=255)
    extra = models.TextField(null=True, blank=True)
    position = models.IntegerField(default=0)
    separator = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def get_extra(self):
        return pickle.loads(base64.decodestring(self.extra))

    def get_value(self):
        if self.type == 'array':
            return self.value.split(',')
        if self.type == 'integer':
            return int(self.value)
        if self.type == 'float':
            return float(self.value)
        if self.type == 'boolean':
            return self.value == "1"
        return self.value

    def set_value(self, value):
        if self.type == 'array':
            self.value = ','.join(value)
        elif self.type == 'integer':
            self.value = int(value)
        elif self.type == 'float':
            self.value = float(value)
        elif self.type == 'boolean':
            self.value = 1 if value else 0
        else:
            self.value = value
        if not self.value and self.value_default:
            self.value = self.value_default
        return self.value

    def get_field(self):
        extra = self.get_extra()

        # Set validators
        field_validators = []
        if 'min' in extra:
            if self.type == 'string' or self.type == 'array':
                field_validators.append(validators.MinLengthValidator(extra['min']))
            if self.type == 'integer' or self.type == 'float':
                field_validators.append(validators.MinValueValidator(extra['min']))
        if 'max' in extra:
            if self.type == 'string' or self.type == 'array':
                field_validators.append(validators.MaxLengthValidator(extra['max']))
            if self.type == 'integer' or self.type == 'float':
                field_validators.append(validators.MaxValueValidator(extra['max']))

        # Yes-no
        if self.input == 'yesno':
            return forms.BooleanField(
                                   initial=self.get_value(),
                                   label=_(self.name),
                                   help_text=_(self.description) if self.description else None,
                                   required=False,
                                   widget=YesNoSwitch,
                                   )

        # Multi-list
        if self.input == 'mlist':
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
        if self.input == 'select' or self.input == 'choice':
            # Timezone list?
            if extra['choices'] == '#TZ#':
                extra['choices'] = tzlist()
            return forms.ChoiceField(
                                     initial=self.get_value(),
                                     label=_(self.name),
                                     help_text=_(self.description) if self.description else None,
                                     widget=forms.RadioSelect if self.input == 'choice' else forms.Select,
                                     validators=field_validators,
                                     required=False,
                                     choices=extra['choices']
                                     )

        # Textarea
        if self.input == 'textarea':
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
        if self.type == 'integer':
            default_input = forms.IntegerField
        if self.type == 'float':
            default_input = forms.FloatField

        # Make text-input
        return default_input(
                             initial=self.get_value(),
                             label=_(self.name),
                             help_text=_(self.description) if self.description else None,
                             validators=field_validators,
                             required=False,
                             )
