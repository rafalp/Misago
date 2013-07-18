from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class SignInForm(Form):
    user_email = forms.EmailField(max_length=255, label=_("Your email"))
    user_password = forms.CharField(widget=forms.PasswordInput, max_length=255, label=_("Your password"))
    user_remember_me = forms.BooleanField(label=_("Stay Signed In"), help_text=_("Sign me In automatically next time"), required=False)

    def __init__(self, *args, **kwargs):
        show_remember_me = kwargs.pop('show_remember_me')

        super(SignInForm, self).__init__(*args, **kwargs)
        if not show_remember_me:
            del self.fields['user_remember_me']
