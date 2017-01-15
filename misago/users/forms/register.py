from misago.core import forms

from .. import validators


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[validators.validate_username])
    email = forms.CharField(validators=[validators.validate_email])
    password = forms.CharField(validators=[validators.validate_password],
                               widget=forms.PasswordInput(render_value=True))

    # placeholder field for setting captcha errors on form
    captcha = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        validators.validate_new_registration(self.request, self, cleaned_data)

        return cleaned_data
