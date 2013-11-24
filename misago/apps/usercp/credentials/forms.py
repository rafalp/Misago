import hashlib
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form
from misago.models import User
from misago.validators import validate_password, validate_email

class CredentialsChangeForm(Form):
    new_email = forms.EmailField(label=_('New E-mail'),
                                 help_text=_("Enter new e-mail address or leave this field empty if you want only to change your password."),
                                 max_length=255, required=False)
    new_password = forms.CharField(label=_('New Password'),
                                   help_text=_("Enter new password or leave this empty if you only want to change your e-mail address."),
                                   max_length=255, widget=forms.PasswordInput, required=False)
    current_password = forms.CharField(label= _('Current Password'),
                                       help_text=_("Confirm changes by entering your current password."),
                                       max_length=255, widget=forms.PasswordInput)

    def clean_new_email(self):
        if self.cleaned_data['new_email']:
            new_hash = hashlib.md5(self.cleaned_data['new_email'].lower()).hexdigest()
            if new_hash == self.request.user.email_hash:
                raise ValidationError(_("New e-mail is same as your current e-mail."))
            try:
                User.objects.get(email_hash=new_hash)
                raise ValidationError(_("New e-mail address is already in use by other member."))
            except User.DoesNotExist:
                pass
            validate_email(self.cleaned_data['new_email'])
        return self.cleaned_data['new_email'].lower()

    def clean_new_password(self):
        if self.cleaned_data['new_password']:
            validate_password(self.cleaned_data['new_password'])
        return self.cleaned_data['new_password']

    def clean_current_password(self):
        if not self.request.user.check_password(self.cleaned_data['current_password']):
            raise ValidationError(_("You have entered wrong password."))
        return ''

    def clean(self):
        cleaned_data = super(CredentialsChangeForm, self).clean()
        if not cleaned_data['new_email'] and not cleaned_data['new_password']:
            raise ValidationError(_("You have to enter either new e-mail address or new password."))
        return cleaned_data
