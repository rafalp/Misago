import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form
from misago.utils.timezones import tzlist

class UserForumOptionsForm(Form):
    newsletters = forms.BooleanField(label=_("Newsletters"),
                                     help_text=_("On occasion board administrator may want to send e-mail message to multiple members."),
                                     required=False)
    timezone = forms.ChoiceField(label=_("Your Current Timezone"),
                                 help_text=_("If dates and hours displayed by forums are inaccurate, you can fix it by adjusting timezone setting."),
                                 choices=tzlist())
    hide_activity = forms.TypedChoiceField(label=_("Your Visibility"),
                                           help_text=_("If you want to, you can limit other members ability to track your presence on forums."),
                                           choices=(
                                                    (0, _("Show my presence to everyone")),
                                                    (1, _("Show my presence to people I follow")),
                                                    (2, _("Show my presence to nobody")),
                                                    ), coerce=int)
    subscribe_start = forms.TypedChoiceField(label=_("Threads I start"),
                                             choices=(
                                                      (0, _("Don't watch")),
                                                      (1, _("Put on watched threads list")),
                                                      (2, _("Put on watched threads list and e-mail me when somebody replies")),
                                                      ), coerce=int)
    subscribe_reply = forms.TypedChoiceField(label=_("Threads I reply to"),
                                             choices=(
                                                      (0, _("Don't watch")),
                                                      (1, _("Put on watched threads list")),
                                                      (2, _("Put on watched threads list and e-mail me when somebody replies")),
                                                      ), coerce=int)
    allow_pds = forms.TypedChoiceField(label=_("Allow Private Threads Invitations"),
                                       help_text=_("If you wish, you can restrict who can invite you to private threads. Keep in mind some groups or members may be allowed to override this preference."),
                                       choices=(
                                                (0, _("From everyone")),
                                                (1, _("From everyone but not members I ignore")),
                                                (2, _("From members I follow")),
                                                (2, _("From nobody")),
                                                ), coerce=int)
