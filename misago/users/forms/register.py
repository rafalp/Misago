from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .. import validators


class RegisterForm(forms.Form):
    username = forms.CharField(validators=[validators.validate_username])
    email = forms.CharField(validators=[validators.validate_email])
    password = forms.CharField()

    # placeholder field for setting captcha errors on form
    captcha = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def full_clean_password(self, cleaned_data):
        if cleaned_data.get('password'):
            UserModel = get_user_model()
            validate_password(
                cleaned_data['password'],
                user=UserModel(
                    username=cleaned_data.get('username'),
                    email=cleaned_data.get('email'),
                )
            )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        try:
            self.full_clean_password(cleaned_data)
        except forms.ValidationError as e:
            self.add_error('password', e)

        validators.validate_new_registration(self.request, self, cleaned_data)

        return cleaned_data
