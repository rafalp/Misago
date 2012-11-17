from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class SignInForm(Form):
    user_email = forms.EmailField(max_length=255, label=_("Your email"))
    user_password = forms.CharField(max_length=255, label=_("Your password"))
    user_remember_me = forms.BooleanField(label=_("Stay Signed In"), help_text=_("Sign me In automatically next time"), required=False)
    user_stay_hidden = forms.BooleanField(label=_("Sign In as Hidden"), help_text=_("Dont show me on any on-line lists"), required=False)
    
    def __init__(self, *args, **kwargs):
        show_remember_me = kwargs['show_remember_me']
        show_stay_hidden = kwargs['show_stay_hidden']
        del kwargs['show_remember_me']
        del kwargs['show_stay_hidden']
        
        super(SignInForm, self).__init__(*args, **kwargs)
        if not show_remember_me:
            del self.fields['user_remember_me']
        if not show_stay_hidden:
            del self.fields['user_stay_hidden']
    
    class Meta:
        widgets = {
            'user_password': forms.PasswordInput(),
        }