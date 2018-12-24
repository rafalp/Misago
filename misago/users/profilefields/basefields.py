from django import forms
from django.db.models import Q
from django.utils import html

from ...core.utils import format_plaintext_for_html

__all__ = [
    "ProfileField",
    "TextProfileField",
    "UrlProfileField",
    "TextareaProfileField",
    "ChoiceProfileField",
]


class ProfileField:
    """
    Basic profile field
    """

    fieldname = None
    label = None
    help_text = None
    readonly = False

    def is_editable(self, request, user):
        return not self.readonly

    def get_label(self, user):
        if not self.label:
            raise NotImplementedError(
                "profile field class has to define label "
                "attribute or get_label(user) method"
            )
        return self.label

    def get_help_text(self, user):
        return self.help_text

    def get_form_field(self, request, user):
        return None

    def get_form_field_json(self, request, user):
        return {
            "fieldname": self.fieldname,
            "label": self.get_label(user),
            "help_text": self.get_help_text(user),
            "initial": user.profile_fields.get(self.fieldname, ""),
            "input": self.get_input_json(request, user),
        }

    def get_input_json(self, request, user):
        return None

    def clean(self, request, user, data):
        return data

    def get_display_data(self, request, user):
        value = user.profile_fields.get(self.fieldname, "").strip()
        if not self.readonly and not value:
            return None

        data = self.get_value_display_data(request, user, value)
        if not data:
            return None

        data.update({"fieldname": self.fieldname, "name": str(self.get_label(user))})

        return data

    def get_value_display_data(self, request, user, value):
        return {"text": value}

    def search_users(self, criteria):
        if self.readonly:
            return None

        return Q(**{"profile_fields__%s__contains" % self.fieldname: criteria})


class ChoiceProfileField(ProfileField):
    choices = None

    def get_choices(self, user=None):
        if not self.choices:
            raise NotImplementedError(
                "profile field ChoiceProfileField has to define "
                "choices attribute or get_choices(user) method"
            )
        return self.choices

    def get_form_field(self, request, user):
        return forms.ChoiceField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            choices=self.get_choices(user),
            disabled=self.readonly,
            required=False,
        )

    def get_input_json(self, request, user):
        choices = []
        for key, choice in self.get_choices():  # pylint: disable=not-an-iterable
            choices.append({"value": key, "label": choice})

        return {"type": "select", "choices": choices}

    def get_value_display_data(self, request, user, value):
        for key, name in self.get_choices():  # pylint: disable=not-an-iterable
            if key == value:
                return {"text": str(name)}

    def search_users(self, criteria):
        """custom search implementation for choice fields"""
        q_obj = Q(**{"profile_fields__%s__contains" % self.fieldname: criteria})

        for key, choice in self.get_choices():  # pylint: disable=not-an-iterable
            if key and criteria.lower() in str(choice).lower():
                q_obj = q_obj | Q(**{"profile_fields__%s" % self.fieldname: key})

        return q_obj


class TextProfileField(ProfileField):
    def get_form_field(self, request, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )

    def get_input_json(self, request, user):
        return {"type": "text"}


class TextareaProfileField(ProfileField):
    def get_form_field(self, request, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=500,
            widget=forms.Textarea(attrs={"rows": 4}),
            disabled=self.readonly,
            required=False,
        )

    def get_input_json(self, request, user):
        return {"type": "textarea"}

    def get_value_display_data(self, request, user, value):
        return {"html": html.linebreaks(html.escape(value))}


class UrlifiedTextareaProfileField(TextareaProfileField):
    def get_value_display_data(self, request, user, value):
        return {"html": format_plaintext_for_html(value)}


class UrlProfileField(TextProfileField):
    def get_form_field(self, request, user):
        return forms.URLField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.profile_fields.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )

    def get_value_display_data(self, request, user, value):
        return {"text": value, "url": value}
