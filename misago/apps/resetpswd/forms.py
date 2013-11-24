import hashlib
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, QACaptchaField, ReCaptchaField
from misago.models import User

class UserResetPasswordForm(Form):
    email = forms.EmailField(label=_("Your E-mail Address"),
                             help_text=_("Enter email address password reset confirmation e-mail will be sent to. It must be valid e-mail you used to register on forums."),
                             max_length=255)
    captcha_qa = QACaptchaField()
    recaptcha = ReCaptchaField()
    error_source = 'email'

    def clean_email(self):
        try:
            email = self.cleaned_data['email'].lower()
            email_hash = hashlib.md5(email).hexdigest()
            self.found_user = User.objects.get(email_hash=email_hash)
        except User.DoesNotExist:
            raise ValidationError(_("There is no user with such e-mail address."))
        return email