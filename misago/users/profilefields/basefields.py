from django import forms


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

    def admin_update_extra(self, user, cleaned_data):
        if self.readonly:
            return

        user.extra[self.fieldname] = cleaned_data.get(self.fieldname)


class ChoiceProfileField(ProfileField):
    choices = None

    def get_choices(self, user):
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
            initial=user.extra.get(self.fieldname),
            choices=self.get_choices(user),
            disabled=self.readonly,
            required=False,
        )


class TextProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )


class TextareaProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            widget=forms.Textarea(
                attrs={'rows': 4},
            ),
            disabled=self.readonly,
            required=False,
        )


class SlugProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.SlugField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )


class UrlProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.URLField(
            label=self.get_label(user),
            help_text=self.get_help_text(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            disabled=self.readonly,
            required=False,
        )
