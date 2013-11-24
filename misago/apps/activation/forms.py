import hashlib
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form, QACaptchaField, ReCaptchaField
from misago.models import User

class UserSendActivationMailForm(Form):
    email = forms.EmailField(max_length=255)
    captcha_qa = QACaptchaField()
    recaptcha = ReCaptchaField()
    error_source = 'email'

    layout = [
              (
               None,
               [('email', {'label': _("Your E-mail Address"), 'help_text': _("Enter email address send activation e-mail to. It must be valid e-mail you used to register on forums."), 'attrs': {'placeholder': _("Enter your e-mail address.")}})]
               ),
              (
               None,
               ['captcha_qa', 'recaptcha']
               ),
              ]

    def clean_email(self):
        try:
            email = self.cleaned_data['email'].lower()
            email_hash = hashlib.md5(email).hexdigest()
            self.found_user = User.objects.get(email_hash=email_hash)
        except User.DoesNotExist:
            raise ValidationError(_("There is no user with such e-mail address."))
        return email
