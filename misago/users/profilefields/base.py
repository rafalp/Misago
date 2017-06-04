from django import forms


class ProfileField(object):
    """
    Basic profile field
    """
    fieldname = None
    label = None

    def get_label(self, user):
        if not self.label:
            raise NotImplementedError(
                "profile field class has to define label "
                "attribute or get_label(user) method"
            )
        return self.label

    def extend_admin_form(self, form, user):
        return form


class TextProfileField(ProfileField):
    def extend_admin_form(self, form, user):
        fieldname = self.fieldname

        return type('TextProfileFieldForm', (form,), {
            fieldname: self.get_admin_form_field(
                user, fieldname, self.get_label(user)),
            'clean_{}'.format(fieldname): self.get_admin_form_field_clean(
                user, fieldname),
        })

    def get_admin_form_field(self, user, fieldname, label):
        return forms.CharField(
            label=label,
            initial=user.extra.get(fieldname),
            max_length=250,
            required=False,
        )

    def get_admin_form_field_clean(self, user, fieldname):
        def clean_field(self):
            data = self.cleaned_data.get(fieldname)
            user.extra[fieldname] = data
            return data
        return clean_field


class TextareaProfileField(TextProfileField):
    pass
