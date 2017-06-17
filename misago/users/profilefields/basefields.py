from django import forms
from django.db.models import Q
from django.utils import html
from django.utils.six import text_type

from misago.core.utils import format_plaintext_for_html


__all__ = [
    'ProfileField',
    'TextProfileField',
    'UrlProfileField',
    'TextareaProfileField',
    'ChoiceProfileField',
]


class ProfileField(object):
    """
    Basic profile field
    """
    fieldname = None
    label = None
    help_text = None
    readonly = False

    def get_label(self, user):
        if not self.label:
            raise NotImplementedError(
                "profile field class has to define label "
                "attribute or get_label(user) method"
            )
        return self.label

    def get_help_text(self, user):
        return self.help_text

    def get_admin_field(self, user):
        return None

    def clean_admin_form(self, form, data):
        return data

    def admin_update_profile_fields(self, user, cleaned_data):
        if self.readonly:
            return

        user.profile_fields[self.fieldname] = cleaned_data.get(self.fieldname)

    def admin_search(self, criteria, queryset):
        return Q(**{
            'profile_fields__{}__contains'.format(self.fieldname): criteria
        })

    def get_data(self, request, user):
        field_data = user.profile_fields.get(self.fieldname)
        if not len(field_data):
            return None

        data = self.get_display_data(request, user, field_data)
        if not data:
            return None

        data['name'] = text_type(self.get_label(user))

        return data

    def get_display_data(self, request, user, data):
        return {
            'text': data
        }

    def can_edit(self, request, user):
        return not self.readonly


class ChoiceProfileField(ProfileField):
    choices = None

    def get_choices(self, user=None):
        if not self.choices:
            raise NotImplementedError(
                "profile field ChoiceProfileField has to define "
                "choices attribute or get_choices(user) method"
            )
        return self.choices

    def get_admin_field(self, user):
        return forms.ChoiceField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            choices=self.get_choices(user),
            disabled=self.readonly,
            required=False,
        )

    def admin_search(self, criteria, queryset):
        """custom search implementation for choice fields"""
        q_obj = Q(**{
            'profile_fields__{}__contains'.format(self.fieldname): criteria
        })

        for key, choice in self.get_choices():
            if key and criteria.lower() in text_type(choice).lower():
                q_obj = q_obj | Q(**{
                    'profile_fields__{}'.format(self.fieldname): key
                })

        return q_obj

    def get_display_data(self, request, user, data):
        for key, name in self.get_choices():
            if key == data:
                return {
                    'text': text_type(name),
                }
        return None


class TextProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )


class TextareaProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            widget=forms.Textarea(
                attrs={'rows': 4},
            ),
            disabled=self.readonly,
            required=False,
        )

    def get_display_data(self, request, user, data):
        return {
            'html': html.linebreaks(html.escape(data)),
        }


class UrlifiedTextareaProfileField(TextareaProfileField):
    def get_display_data(self, request, user, data):
        return {
            'html': format_plaintext_for_html(data),
        }


class SlugProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.SlugField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )

    def get_display_data(self, request, user, data):
        return {
            'text': data,
            'url': data,
        }


class UrlProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.URLField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )

    def get_display_data(self, request, user, data):
        return {
            'text': data,
            'url': data,
        }
