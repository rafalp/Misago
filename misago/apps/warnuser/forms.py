from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form

class WarnMemberForm(Form):
    reason = forms.CharField(label=_("Warning reason"), max_length=2048)
