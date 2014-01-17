from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.conf import settings
from misago.forms import Form, QACaptchaField, ReCaptchaField, ForumTOS
from misago.models import User
from misago.utils.timezones import tzlist
from misago.validators import validate_username, validate_password, validate_email

class UserRegisterForm(Form):
    username = forms.CharField(label=_('Username'),
                               max_length=15)
    email = forms.EmailField(label=_('E-mail address'),
                             help_text=_("Working e-mail inbox is required to maintain control over your forum account."),
                             max_length=255)
    email_rep = forms.EmailField(max_length=255)
    password = forms.CharField(label=_('Password'),
                               help_text=_("Password you will be using to sign in to your account. Make sure it's strong."),
                               max_length=255,widget=forms.PasswordInput)
    password_rep = forms.CharField(max_length=255,widget=forms.PasswordInput)
    captcha_qa = QACaptchaField()
    recaptcha = ReCaptchaField()
    accept_tos = forms.BooleanField(label=_("Forum Terms of Service"),
                                    required=True, widget=ForumTOS,
                                    error_messages={'required': _("Acceptation of board ToS is mandatory for membership.")})

    validate_repeats = (('email', 'email_rep'), ('password', 'password_rep'))
    repeats_errors = [{
                       'different': _("Entered addresses do not match."),
                       },
                      {
                       'different': _("Entered passwords do not match."),
                       }]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        help_text_formats = {
                             'min': settings_lazy.username_length_min,
                             'max': settings_lazy.username_length_max,
                            }
        self.fields['username'].help_text = _(
            "Your displayed username. Between %(min)s and %(max)s characters, only letters and digits are allowed.") % help_text_formats

    def finalize_form(self):
        if not settings.tos_url and not settings.tos_content:
            del self.fields['accept_tos']

    def clean_username(self):
        validate_username(self.cleaned_data['username'])
        new_user = User.objects.get_blank_user()
        new_user.set_username(self.cleaned_data['username'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_username_valid(e)
        return self.cleaned_data['username']

    def clean_email(self):
        new_user = User.objects.get_blank_user()
        new_user.set_email(self.cleaned_data['email'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_email_valid(e)
        return self.cleaned_data['email']

    def clean_password(self):
        validate_password(self.cleaned_data['password'])
        new_user = User.objects.get_blank_user()
        new_user.set_password(self.cleaned_data['password'])
        try:
            new_user.full_clean()
        except ValidationError as e:
            new_user.is_password_valid(e)
        return self.cleaned_data['password']