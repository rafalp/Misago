from django import forms


class ProfileField(object):
    """
    Basic profile field
    """
    fieldname = None
    label = None
    readonly = False

    def get_label(self, user):
        if not self.label:
            raise NotImplementedError(
                "profile field class has to define label "
                "attribute or get_label(user) method"
            )
        return self.label

    def get_admin_field(self, user):
        return None

    def clean_admin_form(self, form, data):
        return data

    def admin_update_extra(self, user, cleaned_data):
        if self.readonly:
            return
        user.extra[self.fieldname] = cleaned_data.get(self.fieldname)


class TextProfileField(ProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            required=False,
        )


class TextareaProfileField(TextProfileField):
    def get_admin_field(self, user):
        return forms.CharField(
            label=self.get_label(user),
            initial=user.extra.get(self.fieldname),
            max_length=250,
            widget=forms.Textarea(
                attrs={'rows': 4},
            ),
            required=False,
        )
