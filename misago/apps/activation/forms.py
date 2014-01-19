import hashlib
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, QACaptchaField, ReCaptchaField
from misago.models import User

class UserSendActivationMailForm(Form):
    email = forms.EmailField(label=_("Your E-mail Address"),
                             help_text=_("Enter email address send activation e-mail to. It must be valid e-mail you used to register on forums."),
                             max_length=255)
    captcha_qa = QACaptchaField()
    recaptcha = ReCaptchaField()
    error_source = 'email'

    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            self.found_user = User.objects.get_by_email(data)
        except User.DoesNotExist:
            raise ValidationError(_("There is no user with such e-mail address."))
        return data
