from misago.core import forms
from misago.users import validators


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[validators.validate_username])
    email = forms.CharField(validators=[validators.validate_email])
    password = forms.CharField(validators=[validators.validate_password],
                               widget=forms.PasswordInput(render_value=True))

    # placeholder field for setting captcha errors on form
    captcha = forms.CharField(required=False)
