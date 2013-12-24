from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.forms import Form, YesNoSwitch
from misago.models import WarnLevel
from misago.validators import validate_sluggable

class WarnLevelForm(Form):
    name = forms.CharField(label=_("Warning Level Name"),
                           max_length=255, validators=[validate_sluggable(
                                                                          _("Warning level name must contain alphanumeric characters."),
                                                                          _("Warning level name is too long.")
                                                                          )])
    description = forms.CharField(label=_("Warning Level Description"),
                                  help_text=_("Optional message displayed to members with this warning level."),
                                  widget=forms.Textarea, required=False)
    expires_after_minutes = forms.IntegerField(label=_("Warning Level Expiration"),
                                               help_text=_("Enter number of minutes since this warning level was imposed on member until it's reduced and lower level is imposed, or 0 to make this warning level permanent."),
                                               initial=0, min_value=0)
    inhibit_posting_replies = forms.TypedChoiceField(label=_("Restrict Replies Posting"),
                                                     choices=(
                                                        (0, _("No restrictions")),
                                                        (1, _("Review by moderator")),
                                                        (2, _("Disallowed")),
                                                     ),
                                                     coerce=int, initial=0)
    inhibit_posting_threads = forms.TypedChoiceField(label=_("Restrict Threads Posting"),
                                                     choices=(
                                                        (0, _("No restrictions")),
                                                        (1, _("Review by moderator")),
                                                        (2, _("Disallowed")),
                                                     ),
                                                     coerce=int, initial=0)
