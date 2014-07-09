from django.utils.translation import ugettext_lazy as _
from misago.core import forms
from misago.users import validators


class RegisterForm(forms.Form):
    captcha_setting = 'captcha_on_registration'

    username = forms.CharField(label=_("Username"),
                               validators=[validators.validate_username])
    email = forms.CharField(label=_("Email"),
                            validators=[validators.validate_email])
    password = forms.CharField(label=_("Password"),
                               validators=[validators.validate_password],
                               widget=forms.PasswordInput(render_value=True))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.api_fields = (
            (self['username'], 'misago:api_validate_username'),
            (self['email'], 'misago:api_validate_email'),
            (self['password'], 'misago:api_validate_password'),
        )
